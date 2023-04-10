import Vue from 'vue'
import VueI18n from 'vue-i18n'
import elementZh from 'element-ui/lib/locale/lang/zh-CN'
import elementEN from 'element-ui/lib/locale/lang/en'
import cn from './zh_CN'
import en from './en_US'
 
Vue.use(VueI18n)
 
export default new VueI18n({
    locale:  window.localStorage.getItem('user_lang'),
    // 语言标识
    messages: {
        'cn': {
        ...cn,
        ...elementZh
        },   // 中文语言包
        'en': {
        ...en,
        ...elementEN
        }   // 英文语言包
    }
})