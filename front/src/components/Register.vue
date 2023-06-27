<template>
  <div class="login-wrap">
    <div class="name-title">招聘数据分析平台</div>
    <div class="inner">
      <div class="login-box">
        <div class="user-login">欢迎注册</div>
        <div class="login-tip">
          WELCOME TO REGISTER
        </div>
        <div class="login-code-box">
          <div class="input-title">用户名</div>
          <div class="login-number-box">
              <img class="login-icon" src="../assets/images/l-count.png" alt="">
              <input type="text" v-model="number" placeholder="请输入用户名" >
          </div>
        </div>
        <div class="login-code-box">
          <div class="input-title">密码</div>
          <div class="login-number-box">
            <img class="login-icon" src="../assets/images/l-password.png" alt="">
            <input type="password" v-model="getcode" placeholder="请输入密码">
          </div>
        </div>
        <div class="login-code-box">
          <div class="input-title">确认密码</div>
          <div class="login-number-box">
            <img class="login-icon" src="../assets/images/l-password.png" alt="">
            <input type="password" v-model="getcode_recheck" placeholder="请输入密码">
          </div>
        </div>
        <button class="login-btn" @click="RegisterBtn" >注册</button>
        <div class="account-box">
          已有账户？<span @click="goLoginPage">去登录</span>
        </div>
      </div>
    </div>
    
    
  </div>
</template>

<script>
export default {
  data(){
    return{
      number: "",
      getcode: "",
      checkcode: "",
      image_code_url: "",
      uuid: "",
      getcode_recheck: ""
    }
  },
  watch:{
    //输入账号
    'number'(newval) {
      if(newval.length !== 0) {
       
      }
    },
    //输入密码
    'getcode'(newval) {
      if (newval.length !== 0) {
      }
    },
    //确认密码
    'getcode_recheck'(newval) {
      if (newval.length !== 0) {
      }
    }
  },
  created(){
  },
  methods: {
    RegisterBtn(){
      if(this.number && this.getcode && this.getcode_recheck){
        if (this.getcode != this.getcode_recheck) {
          alert('密码不一致，请重新输入！')
        } else {
          this.$http.post('/user/registry',{
            username: this.number,
            password: this.getcode
          }).then(res=>{
            console.log(res,' 注册')
            if(res.code == 200){
              this.$router.replace('/')
              alert(res.data)
            }else {
              alert(res.data)
            }
          })
        }
      } else {
        alert('请将注册信息填写完整！')
      }
    },
    goLoginPage(){
      this.$router.replace('/')
    }
  }
}
</script>

<style scoped>

.login-wrap{
  width: 100%;
  height: 100vh;
  background: url('../assets/images/bg.jpg') no-repeat;
  background-size: 100% 100%;
  position: relative;
}

.inner{
  width: 330px;
  height: 480px;
  position: absolute;
  top: 50%;
  left: 66%;
  margin-top: -240px;
  border-radius: 10px;

}

.name-title{
  text-align: center;
  font-size: 64px;
  font-weight: 600;
  color: #fff;
  position: absolute;
  top: 6%;
  left: 54%;
}

.bg-img img{
  width: 100%;
  height: 100%;
  border-radius: 10px;
}
  

.login-box{
  width:350px;
  height: 460px;
  border-radius: 10px;
  padding:0px 20px;
  box-sizing: border-box;
  background: #fff;
  box-shadow: 4px 4px 10px rgb(133, 113, 241);
}
.user-login{
  padding-top: 30px;
  box-sizing: border-box;
  font-size: 20px;
  color:rgb(47 81 229 / 80%);
  text-align: center;
  font-weight: 888;
  letter-spacing: 8px;
}
.login-tip{
  padding: 10px 0px 24px 0px;
  box-sizing: border-box;
  text-align: center;
  font-size: 12px;
  color:rgb(127, 129, 131);
  letter-spacing: 2px;
}
.getcode-box{
  margin-top: 25px;
  display: flex;
  justify-content: space-between;
}
.inputcode{
  width: 70%;
}
.inputcode-btn-box{
  width: 25%;
}
.inputcode-btn-box img{
  height:calc(1.5em + 0.75rem + 2px);
}
.cundown-box{
  position: relative;
}
.cutdown-text{
  display: block;
  width: 100%;
  text-align: center;
  line-height:calc(1.5em + 0.75rem + 2px); ;
  position: absolute;
  top:0;
  left:0;
  color:rgb(127, 129, 131);;
  z-index:455;
}

.input-title{
  font-size: 15px;
  color: rgb(47 81 229 / 80%);
  font-weight: 600;
  margin-bottom: 5px;
  margin-left: 20px;
}
.login-number-box{
    width: 250px;
    height: 38px;
    margin: 0 auto;
    margin-bottom: 14px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    border: 1px solid #ccc;
    padding: 0 8px;
    box-sizing: border-box;
    
}
.login-number-box .login-icon{
  width: 14px;
}
.login-number-box input{
  border:none;
  height: 38px;
  background: transparent;
  outline: 0;
  margin-left: 8px;
  color:#ccc;
  font-size: 18px;
  -webkit-appearance:none; 
}
.login-number-box input::-webkit-input-placeholder{
  color:#cdcdcd;
  font-size: 14px;
}
.sort-input{
  width: 180px;
  
}
.sort-input input{
  width: 150px!important;
}
.another-login{
  display: flex;
  justify-content: center;
  
}
.another-login img{
  width: 24px;
}
.yanzheng{
  background: #ccc;
  width: 90px; 
  height: 42px; 
  line-height: 42px;
}

.login-btn{
  width: 250px;
  height: 32px;
  margin-left: 20px;
  border-radius: 20px;
  border:none;
  margin-top: 12px;
  outline: 0;
  font-size: 14px;
  color:#fff;
  font-weight: 600;
  letter-spacing: 4px;
  background: rgb(47 81 229 / 80%);
}
    

.btn-box{
  display: flex;
  flex-wrap: column;
  align-items: center;
  margin-top: 25px;
  
}
.btn-box button{
  width: 100%;
  border-radius: none;
  margin: 0 auto;
}
.account-box{
  width: 100%;
  display: flex;
  justify-content: flex-end;
  color: rgb(127, 129, 131);
  font-size: 12px;
  margin-top: 20px;
}
.account-box span{
  color: rgb(127, 129, 131);
  font-weight: 600;
}
.account-box span:hover{
  cursor: pointer;
}


</style>
