import axios from 'axios'

const request = axios.create({
  baseURL: 'http://106.52.123.19:8000',
  timeout: 8000,
  // retry:2,
  // retryDelay:1000
})

// 添加请求拦截
request.interceptors.request.use(function (config) {
  if(config.url.includes("http")){
    // 自定义以@符分隔  baseURL@url
    let arr =config.url.split('@')
    config.url = arr[1]
    config.baseURL= arr[0]
  }
  return {
    ...config,
    headers: {
      ...config.headers,
    }
  }
  // 发送请求之前做些什么
  
}, function (error) {
  return Promise.reject(error)
})

// 添加响应拦截器

request.interceptors.response.use((response)=> {
  return response.data
}, (error)=> {
  const response = error.response
  const status = response.status
  if (status < 500) {
    switch (status) {
      case 400:  
      break;
      case 401:
      localStorage.clear()
      setTimeout(()=>{
        // router.push('/')
      },2000)
      break
      case 422:
        break
      default:
        console.log('报错')
    }
  } else {
    console.log('服务繁忙稍后再试')
  }
  return Promise.reject(response)
})
export default function(Vue){
  Vue.prototype.$http={
    get (url, data = {}) {
      return request.get(url, {params: data
      })
    },
    post (url, data = {}) {
      return request.post(url, data)
    }
  }
}