import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import http from './utils/http'
import router from './router'
import 'element-ui/lib/theme-chalk/index.css';
import '../src/assets/global.css'

Vue.use(ElementUI);
Vue.use(http);
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
