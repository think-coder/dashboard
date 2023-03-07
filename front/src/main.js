import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


const app = createApp(App);                      // 创建app实例
app.use(store)
app.use(router)
app.use(ElementPlus)                            //配置axios的全局引用
app.mount('#app')                               // 将app实例 全局挂载至 app 元素
