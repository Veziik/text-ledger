import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.config.globalProperties.$user = null
app.config.globalProperties.$isLoggedIn = false

app.use(router)
app.mount('#app')