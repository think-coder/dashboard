import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import http from './utils/http'
import router from './router'
import i18n from './assets/i18n/lang'
import 'element-ui/lib/theme-chalk/index.css';
import '../src/assets/global.css'
Vue.use(ElementUI, {
  i18n: (key, value) => i18n.t(key, value)  
});
Vue.use(http);
Vue.config.productionTip = false


new Vue({
  render: h => h(App),
  router,
  i18n
}).$mount('#app')


