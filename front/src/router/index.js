// src/router/index.js 就是当前项目的路由模块

// 1. 导入 Vue 和VueRouter 的包
import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login'
import Register from '../components/Register'
import MainPage from '../components/HelloWorld'
import Teacher from '../components/Teacher'

// 2. 把 VueRouter 安装为 Vue 项目的插件
// Vue.use() 函数的作用，就是来安装插件的
Vue.use(VueRouter)

// 3. 创建路由的实例对象
const router = new VueRouter({
    // mode:'hash',
    // mode:'history',
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/mainpage',
            name: 'Mainpage',
            component: MainPage
        },
        {
            path: '/register',
            name: 'Register',
            component: Register
            
        },
        {
            path: '/teacher',
            name: 'Teacher',
            component: Teacher
        }
    ]
})

// 4. 向外共享路由实例对象
export default router
