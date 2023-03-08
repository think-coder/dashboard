<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="首页" name="1">
       <el-tabs :tab-position="tabPosition" style="height: 200px;">
        <el-tab-pane label="宁德时代">
          <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="date" label="日期" width="180"></el-table-column>
        </el-table>
  </el-tab-pane>
        <el-tab-pane label="平安银行">平安银行</el-tab-pane>
        <el-tab-pane label="万达电影">万达电影</el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane label="全国招聘数据" name="2">
      <div v-if="activeName==2"><HtmlPanel /></div>
    </el-tab-pane>
    <el-tab-pane label="省级招聘数据" name="3" >
      <el-tabs :tab-position="tabPosition" class="el-tabs-box" @tab-click="handleProviceMap">
        <el-tab-pane v-for="(item, index) in allProvince" :label="item" :key="index" :name="item">
          <span>{{item}}</span>
        </el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane label="一线/新一线" name="5">一线/新一线</el-tab-pane>
    <el-tab-pane label="增长最快" name="6">增长最快</el-tab-pane>
    <el-tab-pane label="下降最快" name="7">下降最快</el-tab-pane>
  </el-tabs>
</template>
<script>
import HtmlPanel from "./HtmlPanel.vue"; //根据实际路径导入
  export default {
    components:{HtmlPanel},
    data() {
      return {
        activeName: '1',
        tabPosition: 'left',
        allProvince:[],
        province:'',
        tableHeader:[{
          prop:"date",
          label:" 股票代码"
        },{
          prop:"date2",
          label:"日期"
        }],
        tableData: [{
           date:1
        },{
           date:2
        }]
      };
    },
    created(){
      this.getIndexData()
      // this.getCountryMap()
    },
    mounted(){
      this.getAllProvince()
    },
    methods: {
      getIndexData(){
        this.$http.get('/dashboard/get_total_employer').then(res=>{
          console.log(res,'res')
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      handleClick(tab, event) {
        console.log(tab, event);
        if(tab.name === '3'){
          this.getProvinceMap(this.province)
        }
      },
      // 获取全国省份
      getAllProvince(){
        this.$http.get('/dashboard/get_all_province').then(res=>{
          console.log(res.data,'获取全国省份')
          this.allProvince = res.data
          this.province = res.data[0]
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      handleProviceMap(e){
        console.log(e.name, 'handleProviceMap')
        this.getProvinceMap(e.name)
      },
      // 获取省份对应地图
      getProvinceMap(name){
        this.$http.get(`/dashboard/get_map_by_province/${name}`).then(res=>{
          console.log(res,'省份对应地图')
          document.write(res);
          document.close();
          // this.allProvince = res.data
          // console.log(this.allProvince, 'this.allProvince')
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      
    }
  };
</script>
<style>
  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  .el-tabs-box{
    height:800px;
  }
</style>
