import { createApp } from "vue"
import { createRouter, createWebHistory } from "vue-router"
import App from "./App.vue"
import Home from "./views/Home.vue"
import Interview from "./views/Interview.vue"
import Summary from "./views/Summary.vue"

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/interview", name: "Interview", component: Interview },
  { path: "/summary", name: "Summary", component: Summary },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount("#app")
