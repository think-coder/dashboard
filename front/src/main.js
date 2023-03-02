import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import http from './utils/http'
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);
Vue.use(http);
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
