<template>
  <div class="teacher-wrap">
    <div class="inner">
        <img style="width:200px" src="../assets/images/teacher-head.png"/>
        <div style="width: 100%; text-align:center;margin-bottom: 12px;">教学评估表</div>
        <div style="width: 100%; text-align:center;margin-bottom: 12px; font-size: 18px; font-weight:600">香港中文大学（深圳）数据经济研究学院***课程教学评估表</div>
        <div style="width: 100%; display:flex; flex-wrap: wrap;">
            <div style="width: 50%; margin-bottom: 12px; font-size: 14px;">主讲老师：<input v-model="teachername" placeholder="请输入" /></div>
            <div style="width: 50%; margin-bottom: 12px; font-size: 14px;">课程名称：<input v-model="coursename" placeholder="请输入" /></div>
            <div style="width: 50%; margin-bottom: 12px; font-size: 14px;">上课班级：<input v-model="classname" placeholder="请输入" /></div>
            <div style="width: 50%; margin-bottom: 12px; font-size: 14px;">上课时间：<input v-model="classtime" placeholder="请输入" /></div>
        </div>
        <table class="gridtable">
            <tr>
                <th>项目</th>
                <th>指标内容</th>
                <th>考评分数（高分->低分）</th>
            </tr>
            <tr>
                <th></th>
                <th></th>
                <th class="score-th">
                    <td class="score-td" v-for="(item, index) in [10,9,8,7,6,5,4,3,2,1]" :key="index">{{item}}</td>
                </th>
            </tr>
            <tr v-for="(item,index) in tableData" :key="index">
                <td class="title">{{item.title}}</td>
                <td class="tr2-td">
                    <tr class="tr2-tr" v-for="(_item,_index) in item.content" :key="_index">{{_item}}</tr>
                </td>
                <td class="tr3-td">
                    <th style="display: flex" class="score-th score-th-content" v-for="(_item,__index) in item.content" :key="_item">
                        <td class="score-td" v-for="(scoreItem, scoreIndex) in [10,9,8,7,6,5,4,3,2,1]" :key="scoreIndex">
                            <input type="radio" :name="item.title+__index" @change="inputchecked(item.title, __index, scoreItem)">
                        </td>
                    </th>
                </td>
            </tr>
            <tr>
                <th class="content-box" colspan="2">对授课老师的总体评分</th>
                <th class="content-box">
                    （<input v-model="score_teacher" class="style-static" />）<span>满分100</span>
                </th>
            </tr>
            <tr>
                <th class="content-box" colspan="2">对课程质量的总体评分</th>
                <th class="content-box">
                    （<input v-model="score_course" type="number" oninput="if(value.length>3)value=value.slice(0,3)" max=100 min=1 class="style-static" />）<span>满分100</span>
                </th>
            </tr>
            <tr>
                <th class="content-box" colspan="2">您对本课程的总体评价</th>
                <th class="content-box">
                    <textarea v-model="course_txt" type="number" oninput="if(value.length>3)value=value.slice(0,3)" max=100 min=1 class="style-static" cols="30" rows="10"></textarea>
                </th>
            </tr>
            <tr>
                <th class="content-box" colspan="2">您对本次课程的建议</th>
                <th class="content-box">
                    <textarea v-model="course_advice" class="style-static" cols="30" rows="10"></textarea>
                </th>
            </tr>
        </table>
        <div style="display: flex; justify-content: flex-end; align-items: center; margin-top: 20px;">
            签名：<input v-model="handsname" style="width: 80px; height: 32px" /> <div class="submit" @click="submitBtn">提交</div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return{
        teachername: "",
        coursename: "",
        classname: "",
        classtime: "",
        handsname: "",
        tableData:{},
        score_teacher:'',
        score_course:'',
        course_txt:'',
        course_advice:'',
        attitude: [],
        content: [],
        effect: [],
        organization:[],
    }
  },
  watch:{
    'teachername'(newval) {
      if(newval.length !== 0) {
       
      }
    },
    'coursename'(newval) {
      if (newval.length !== 0) {
      }
    },
    'classname'(newval) {
      if (newval.length !== 0) {
      }
    },
    'classtime'(newval) {
      if (newval.length !== 0) {
      }
    },
    'handsname'(newval) {
      if (newval.length !== 0) {
      }
    },
    'course_txt'(newval) {
      if (newval.length !== 0) {
      }
    },
    'course_advice'(newval) {
      if (newval.length !== 0) {
      }
    },
    'score_teacher'(newval) {
      if (newval.length !== 0) {
      }
    },
    'score_course'(newval) {
      if (newval.length !== 0) {
      }
    },
  },
  created(){
      this.getData()
  },
  methods: {
    getData(){
        this.$http.get('/edp/table/teach_assess').then(res=>{
            console.log(res,' data')
            this.tableData = res.data
        })
    },
    submitBtn(){
        if (!this.teachername && 
            !this.coursename &&
            !this.classname &&
            !this.classtime &&
            !this.course_txt&&
            !this.course_advice&&
            !this.handsname){
           alert('请将信息填写完整！')
        } else {
          this.$http.post('/edp/table/teach_assess',{
            teacher: this.teachername,
            course: this.coursename,
            class: this.classname,
            time: this.classtime,
            attitude: this.attitude,
            content: this.content,
            effect: this.effect,
            organization:this.organization,
            teacher_score: this.score_teacher,
            course_score: this.score_course,
            appraise: this.course_txt,
            recommend: this.course_advice,
            signature: this.handsname
          }).then(res=>{
            alert("提交成功")
          })
        }
    },
    inputchecked(item, index, score){
        if(item === "教学态度"){
            if(this.attitude.length){
               this.attitude.forEach((at, ai)=>{
                    if( Object.keys(at)[0] == `${item+index}`) {
                         this.attitude =  this.attitude.splice(0,ai)
                    } 
                    this.attitude = this.attitude.concat({[`${item+index}`]: score})
                })
            } else {
                this.attitude = this.attitude.concat({[`${item+index}`]: score})
            }
        } else if(item === "教学内容"){
            if(this.content.length){
               this.content.forEach((at, ai)=>{
                    if( Object.keys(at)[0] == `${item+index}`) {
                         this.content =  this.content.splice(0,ai)
                    } 
                    this.content = this.content.concat({[`${item+index}`]: score})
                })
            } else {
                this.content = this.content.concat({[`${item+index}`]: score})
            }
        } else if(item === "教学效果"){
            if(this.effect.length){
               this.effect.forEach((at, ai)=>{
                    if( Object.keys(at)[0] == `${item+index}`) {
                         this.effect =  this.effect.splice(0,ai)
                    } 
                    this.effect = this.effect.concat({[`${item+index}`]: score})
                })
            } else {
                this.effect = this.effect.concat({[`${item+index}`]: score})
            }
        } else if(item === "教务组织"){
            if(this.organization.length){
               this.organization.forEach((at, ai)=>{
                    if( Object.keys(at)[0] == `${item+index}`) {
                         this.organization =  this.organization.splice(0,ai)
                    } 
                    this.organization = this.organization.concat({[`${item+index}`]: score})
                })
            } else {
                this.organization = this.organization.concat({[`${item+index}`]: score})
            }
        }
    }
  }
}
</script>

<style scoped>
.title{
    width: 100px;

}
.gridtable {
    width: 100%;
    font-family: verdana,arial,sans-serif;
    font-size:11px;
    color:#333333;
    border-width: 1px;
    border-color: #666666;
    border-collapse: collapse;
}
.gridtable th {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #dedede;
    width: 270px;
}
.gridtable td {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #ffffff;
}
.gridtable .tr2-td{
    width: 50%;
    padding: 0;
    box-sizing: border-box;
}
.gridtable .tr2-tr{
    width: 100%;
    height: 30px;
    line-height: 30px;
    border-bottom: 1px solid #666;
    padding: 0 8px!important;
    box-sizing: border-box;
    background-color: #ffffff;
    display: block;
}
.gridtable .tr2-tr:last-child{
    border: 0;
}
.gridtable .tr3-td{
    /* width: 260px; */
    padding: 0;
    box-sizing: border-box;
    border: 0;
}
.gridtable .score-td{
    padding: 0;
    background: none;
    width: 27px;
    height: 30px;
    border-top:0;
    border-bottom: 0;
    border-right: 0;
}
.gridtable .tr3-td .score-th{
   background: none;
   border-left: 0;
   border-top: 0;
   width: 100%;
}
.gridtable .score-td:first-child{
    border-left: 0;
}
.gridtable .score-td:last-child{
    border-right: 0;
}
.gridtable .score-th{
    padding: 0;
    height: 30px;
    line-height: 30px;
}
input{
    padding:2px 4px;
    box-sizing: border-box;
    outline: none;
}
.gridtable .content-box{
    background: none;
    border-top: 0;
    text-align: left;
}
.gridtable .content-box:first-child{
    border-top: 0;
}
.content-box input{
    border: none;
    width: 30px;
    text-align: center;
    outline: none;
}
.content-box textarea{
    border: none;
    height: 50px;
    outline: none;
}
.submit{
    width: 80px;
    height: 32px;
    line-height: 32px;
    text-align: center;
    background: rgb(13,55,94);
    color:#fff;
    font-size: 16px;
    display: inline-block;
    border-radius: 4px;
    margin-left: 12px;
}

@media screen and (max-width: 750px) {
    .teacher-wrap {
        width: 100%;
        margin: 0 auto;
    }
    .inner{
        padding: 20px;
        box-sizing: border-box;
    }
    table .gridtable {
         font-family: verdana,arial,sans-serif;
         font-size:11px;
         color:#333333;
         border-width: 1px;
         border-color: #666666;
         border-collapse: collapse;
     }
     table .gridtable th {
         border-width: 1px;
         padding: 8px;
         border-style: solid;
         border-color: #666666;
         background-color: #dedede;
     }
     table .gridtable td {
         border-width: 1px;
         padding: 8px;
         border-style: solid;
         border-color: #666666;
         background-color: #ffffff;
     }
     .style-static{
         border: none;
         width: 30px;
     }
     .style-static:focus{
         border: none;
     }
}

@media screen and (min-width: 750px) {
    .teacher-wrap {
        margin: 0 auto;
        width: 70%;
    }
    .inner{
        padding: 20px 0;
        box-sizing: border-box;
    }
    
}
</style>
