import os
import logging
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# 兼容OpenAI模式的API地址
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
DASHSCOPE_API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'

INTERVIEW_STYLES = {
    'friendly': {
        'system_prompt': '''你是一位友善、亲切的面试官，像一位耐心的学长学姐。
你的目标是帮助应聘者放松，更好地展示自己。
你必须使用轻松、鼓励性的语言，可以适当使用emoji（如😊👍）。
请针对回答给出具体的、建设性的反馈，并自然地引出下一个问题或追问。
回复必须控制在50-80字之间。''',
    },
    'formal': {
        'system_prompt': '''你是一位专业、严谨的面试官，代表一家注重效率和专业能力的公司。
你的提问和反馈都应直接、客观、切中要点，避免任何情绪化表达。
必须引导应聘者使用STAR法则（情境、任务、行动、结果）来结构化地回答问题。
反馈应侧重于评估其解决问题的能力、专业知识和逻辑思维。
回复必须控制在50-80字之间。''',
    },
    'casual': {
        'system_prompt': '''你是一位随和、健谈的面试官，像是在咖啡馆里与应聘者进行一场非正式交流。
你的风格是对话式的，可以分享一些自己的看法来引导对方。
反馈是启发性的，旨在激发应聘者更深层次的思考，而不是进行严格的评判。
可以使用一些口语化表达，如"嗯，这个想法不错"、"我觉得..."等。
回复必须控制在50-80字之间。''',
    }
}


def call_dashscope_api(messages, max_tokens=150, temperature=0.75):
    """修复兼容模式下的参数格式和响应解析"""
    if not DASHSCOPE_API_KEY:
        logger.error("DASHSCOPE_API_KEY未配置")
        return None, "API密钥未配置，请检查环境变量"

    try:
        logger.info(f"调用通义千问兼容模式API，模型: qwen-turbo，消息前200字: {json.dumps(messages)[:200]}...")

        # 兼容OpenAI模式的请求参数（关键修正）
        response = requests.post(
            DASHSCOPE_API_URL,
            headers={
                'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'qwen-turbo',  # 模型名正确
                # 1. 移除input嵌套，直接传递messages（兼容模式要求）
                'messages': messages,
                # 2. 移除parameters嵌套，参数直接放顶层（兼容模式要求）
                'max_tokens': max_tokens,
                'temperature': temperature,
                'top_p': 0.8
            },
            timeout=30
        )

        logger.info(f"API响应状态码: {response.status_code}")
        logger.info(f"API响应完整内容: {response.text[:1000]}...")

        if response.status_code != 200:
            error_msg = f"API请求失败，状态码: {response.status_code}，响应: {response.text[:500]}"
            logger.error(error_msg)
            return None, error_msg

        result = response.json()
        logger.info(f"API响应JSON结构: {json.dumps(result, indent=2)[:1000]}...")

        # 3. 兼容模式的错误码在error字段（非code字段）
        if 'error' in result:
            error_msg = f"API业务错误: {result['error'].get('message', '无描述')}"
            logger.error(error_msg)
            return None, error_msg

        # 4. 兼容模式的响应结构没有output层，直接是choices（关键修正）
        choices = result.get('choices', [])
        if not choices:
            error_msg = f"API返回空choices，完整响应: {json.dumps(result, indent=2)[:500]}"
            logger.error(error_msg)
            return None, "模型未返回任何结果（空choices）"

        # 5. 兼容模式的content路径不同（关键修正）
        first_choice = choices[0]
        message = first_choice.get('message', {})
        content = message.get('content', '').strip()
        if not content:
            error_msg = f"API返回空content，完整响应: {json.dumps(result, indent=2)[:500]}"
            logger.error(error_msg)
            return None, "模型返回空内容，请检查提示词或模型权限"

        logger.info(f"成功获取内容，长度: {len(content)}，内容前100字: {content[:100]}")
        return content, None

    except requests.exceptions.Timeout:
        error_msg = "API请求超时"
        logger.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_msg = f"处理响应时发生错误: {str(e)}"
        logger.error(error_msg)
        return None, error_msg


@app.route('/api/feedback', methods=['POST'])
def get_feedback():
    try:
        data = request.json
        user_answer = data.get('answer', '').strip()
        question = data.get('question', '').strip()
        style = data.get('style', 'friendly')

        if not user_answer or not question:
            return jsonify({'error': '缺少问题或回答'}), 400

        style_config = INTERVIEW_STYLES.get(style, INTERVIEW_STYLES['friendly'])

        messages = [
            {"role": "system", "content": style_config['system_prompt']},
            {"role": "user",
             "content": f"面试问题：{question}\n\n我的回答是：{user_answer}\n\n请根据我的回答，以面试官的身份给我一些反馈和引导。"}
        ]

        feedback, error = call_dashscope_api(messages, max_tokens=150, temperature=0.75)

        if error:
            return jsonify({'error': error, 'feedback': feedback or '获取反馈失败，请重试'}), 500

        if len(feedback) < 10:
            return jsonify({
                'feedback': feedback,
                'warning': '反馈内容较短，可能不完整'
            }), 200

        return jsonify({'feedback': feedback})

    except Exception as e:
        logger.error(f"处理feedback请求时发生错误: {str(e)}")
        return jsonify({'error': f'服务器处理错误: {str(e)}'}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_performance():
    try:
        data = request.json
        interview_data = data.get('interviewData')

        if not interview_data:
            return jsonify({'error': '缺少面试数据'}), 400

        formatted_data = []
        for i, item in enumerate(interview_data.get('questions', []), 1):
            formatted_data.append(f"问题 {i}: {item.get('text', '')}")
            formatted_data.append(f"回答 {i}: {item.get('answer', '')}")

        formatted_data = "\n".join(formatted_data)

        analysis_prompt = f"""作为资深HR专家，请根据以下面试记录，提供专业、全面的分析报告。

【报告标题】
**面试分析报告**（必须加粗显示）

【报告结构】
1. **一、综合评价**：一句话总结核心优势和需提升点，从沟通风格、思维逻辑、内容深度评价

2. **二、亮点剖析**：2-3个具体优点，每个需引用面试中的具体回答作为证据（格式要求：> "引用的回答内容"）

3. **三、发展建议**：2-3条具体、可执行的改进建议，每条建议需说明**为什么**和**怎么做**

4. **四、潜力预估**：对应聘者职业潜力和发展方向的中肯预估，结合行业趋势给出参考

5. **五、回答结构分析**：评估回答的逻辑性和条理性，是否使用**STAR法则**（情境、任务、行动、结果）等结构化表达

6. **六、岗位匹配度**：基于回答内容推测与目标岗位的匹配程度（如无法判断可说明）

【格式要求】
- 整体内容靠左对齐，不居中
- 标题"面试分析报告"必须用**加粗**
- 主要部分（如综合评价、亮点剖析等）标题需用**加粗**
- 子项使用"1. 2. 3. 4."序号排序
- 面试回答引用必须严格遵循：> "回答内容"（开头用> ，内容加双引号）
- 各部分之间必须用空行（换行符）分隔
- 避免使用###等标题层级符号，全部用序号结构
- "为什么"和"怎么做"需用**加粗**突出显示
- "STAR法则"需用**加粗**突出显示

使用专业、客观且鼓励的语气，避免冰冷评判。对于推测性内容需明确标注"**推测：**"。

面试记录：
{formatted_data}
"""

        messages = [
            {"role": "system", "content": "你是一位资深的HR专家和职业发展顾问，擅长面试分析。"},
            {"role": "user", "content": analysis_prompt}
        ]

        analysis, error = call_dashscope_api(messages, max_tokens=1000, temperature=0.7)

        if error:
            return jsonify({'error': error, 'analysis': analysis or '获取分析失败，请重试'}), 500

        if len(analysis) < 50:
            return jsonify({
                'analysis': analysis,
                'warning': '分析内容较短，可能不完整'
            }), 200

        return jsonify({'analysis': analysis})

    except Exception as e:
        logger.error(f"处理analyze请求时发生错误: {str(e)}")
        return jsonify({'error': f'服务器处理错误: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)