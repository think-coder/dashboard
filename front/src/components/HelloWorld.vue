<template>
<div class="container">
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="首页" name="1">
      <div class="index-wrap">
        <div class="refresh-list-con">
          <el-input placeholder="请输入内容" v-model="searchData" clearable class="input-with-select" style="margin-bottom: 20px;">
            <el-button slot="append" icon="el-icon-search" :disabled="searchData == ''? true : false"  @click="getSearchData" :loading="searchLoading"></el-button>
          </el-input>
          <refresh-list @on-bottom="onBotttom">
            <div v-for="(item, index) in leftPageData" :key="index" class="item-con">
              <div :class="[curLeftData === item ? 'item checked': 'item']" @click="getCheckedData(item)">{{item}}</div>
            </div>
          </refresh-list>
        </div>
        <div>
          <div class="index-content">
            <el-table :data="rightPageData" style="width: 100%;overflow:scroll">
              <el-table-column :fixed="index===1" v-for="(item, index) in tableHeader" :key="index" :prop="item.prop" :label="item.label" width="160"></el-table-column>
              <el-table-column
                fixed="right"
                label="操作"
                width="160">
                    <template slot-scope="scope">
                      <el-button slot="reference" type="text" size="small" @click="handleClickZzDetail(scope.row)">职责范围</el-button>
                      <el-button slot="reference" type="text" size="small" @click="handleClickRzDetail(scope.row)">任职要求</el-button>
                    </template>
              </el-table-column>
            </el-table>
            
          </div>
          <el-pagination
            @current-change="handleCurrentChange"
            :current-page="rightPageNum"
            :page-size="rightPageLimt"
            layout="total, prev, pager, next, jumper"
            :total="rightTotal"
            background
            class="pagination-comp">
          </el-pagination>
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="全国招聘数据" name="2">
      <div v-if="activeName==2"><HtmlPanel :mapSrc="mapSrc"/></div>
    </el-tab-pane>
    <el-tab-pane label="省级招聘数据" name="3" >
      <el-tabs :tab-position="tabPosition" class="el-tabs-box" @tab-click="handleProviceMap">
        <el-tab-pane v-for="(item, index) in allProvince" :label="item" :key="index" :name="item">
          <div v-if="activeName==3 && item==province"><HtmlPanel :mapSrc="mapSrc" /></div>
        </el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane label="一线/新一线" name="4">
      <div v-if="activeName==4"><HtmlPanel :mapSrc="mapSrc"/></div>
    </el-tab-pane>
    <el-tab-pane label="增长最快" name="5">
      <div v-if="activeName==5"><HtmlPanel :mapSrc="mapSrc"/></div>
    </el-tab-pane>
    <el-tab-pane label="下降最快" name="6">
      <div v-if="activeName==6"><HtmlPanel :mapSrc="mapSrc"/></div>
    </el-tab-pane>
  </el-tabs>
  <div class="logout" @click="outlogFn">登出</div>
</div>
</template>
<script>
import HtmlPanel from "./HtmlPanel.vue"; //根据实际路径导入
import RefreshList from "./RefreshList.vue";
  export default {
    components:{
      HtmlPanel,
      RefreshList
    },
    data() {
      return {
        activeName: '1',
        tabPosition: 'left',
        allProvince:[],
        province:'上海市',
        loading: false,
        searchData: '',
        searchLoading: false,
        leftPageData:[],
        leftTotal:0,
        leftPageNum: 1,
        leftPageLimt: 50,
        curLeftData:'',
        rightPageData:[],
        rightTotal:0,
        rightPageNum: 1,
        rightPageLimt: 15,
        mapSrc:'',
        tableHeader:[{
          prop:"股票代码",
          label:"股票代码"
        },{
          prop:"雇主名称",
          label:"雇主名称"
        },{
          prop:"职位名称",
          label:"职位名称"
        },{
          prop:"薪资范围",
          label:"薪资范围"
        },{
          prop:"年薪下限",
          label:"年薪下限"
        },{
          prop:"年薪上限",
          label:"年薪上限"
        },{
          prop:"工作经验要求",
          label:"工作经验要求"
        },{
          prop:"工作地点",
          label:"工作地点"
        },{
          prop:"学历要求",
          label:"学历要求"
        },{
          prop:"发布日期",
          label:"发布日期"
        },{
          prop:"语言要求",
          label:"语言要求"
        },{
          prop:"年龄要求",
          label:"年龄要求"
        },{
          prop:"雇主所在行业",
          label:"雇主所在行业"
        }],
        visible: false
      };
    },
    computed: {
      noMore () {
        return this.leftPageLimt >= this.leftTotal
      },
    },
    watch:{
      'searchData'(newval) {
        if(newval==''){
          this.searchLoading = false
          this.leftPageNum = 1
          this.indexLeftData(this.leftPageNum,this.leftPageLimt)
        }
      },
      'activeName'(newval){
        if(newval == 2){
          this.mapSrc="http://106.52.123.19:58000/dashboard/get_map_by_country/中国"
        } else if(newval == 3){
          console.log(this.province,'province')
          this.mapSrc=`http://106.52.123.19:58000/dashboard/get_map_by_country/${this.province}`
        }else if(newval == 4){
          this.mapSrc="http://106.52.123.19:58000/dashboard/get_map_of_top_city"    
        }else if(newval == 5){
          this.mapSrc="http://106.52.123.19:58000/dashboard/get_map_of_top_rise"
        }else if(newval == 6){
          this.mapSrc="http://106.52.123.19:58000/dashboard/get_map_of_tail_reduce"
        }
      } 
    },
    created(){
      this.indexLeftData(this.leftPageNum, this.leftPageLimt)                            
    },
    mounted(){
      this.getAllProvince()
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },
      // 首页左侧数据
      indexLeftData(num,limt){
        this.$http.get(`/dashboard/get_employer_by_limit/${num}/${limt}`).then(res=>{
          this.leftPageData = this.leftPageData.concat(res.data)
          if(num == 1){
            this.curLeftData = res.data[0]
            this.getRightData(this.curLeftData, this.rightPageNum, this.rightPageLimt)
          }
          this.leftTotal = res.total
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      // 左侧搜索
      getSearchData(){
        if(this.searchData !== ''){
          this.searchLoading = true
          this.$http.get(`/dashboard/get_employer/${this.searchData}`).then(res=>{
            this.leftPageData = res.data
            this.leftTotal = res.total
            this.searchLoading = false
          }).catch(()=>{
            alert('接口错误！')
            this.searchLoading = false
          })
        } else {
          this.indexLeftData(1,this.leftPageLimt)
        }
      },
      // 左侧选中
      getCheckedData(item){
        this.curLeftData = item
        this.rightPageNum = 1
        this.rightPageLimt = 50
        this.getRightData(item,this.rightPageNum,this.rightPageLimt)
      },
      // 左侧加载
      onBotttom() {
        this.leftPageNum = this.leftPageNum + 1
        this.indexLeftData(this.leftPageNum, this.leftPageLimt)
      },
      // 首页右侧数据
      getRightData(_curLeftData,_rightPageNum,_rightPageLimt){
        this.$http.get(`/dashboard/get_employer_data_by_limit/${_curLeftData}/${_rightPageNum}/${_rightPageLimt}`).then(res=>{
          this.rightPageData= res.data
          this.rightTotal = res.total
        }).catch(()=>{
          alert('接口错误！')
          this.searchLoading = false
        })
      },
      // 右侧分页
      handleCurrentChange(val) {
        this.getRightData(this.curLeftData, val, this.rightPageLimt)
      },
      // 右侧查看详情
      handleClickZzDetail(row) {
        this.$alert(row.pos_require, '职责范围', {
          confirmButtonText: '确定',
        });
        console.log(row);
      },
      handleClickRzDetail(row) {
        this.$alert(row.pos_text, '任职要求', {
        });
      },
      // 获取全国省份
      getAllProvince(){
        this.$http.get('/dashboard/get_all_province').then(res=>{
          this.allProvince = res.data
          this.province = res.data[0]
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      handleProviceMap(e){
        this.province = e.name
        this.mapSrc=`http://106.52.123.19:58000/dashboard/get_map_by_country/${this.province}`
      },
      outlogFn(){
        this.$http.post('/dashboard/logout',{
          username: this.$route.query.username
        }).then(res=>{
          console.log(res,' 登录')
          if(res.code == 200) this.$router.replace('/')
        }).catch(()=>{
          alert('接口错误！')
        })
      }
    }
  };
</script>
<style>
  .container{
    width: 100%;
    height: 100vh;
    padding: 6px 10px;
    box-sizing: border-box;
  }
  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  .el-tabs-box-1{
    width: 280px;
    height: 700px;
  }
  .el-tabs-box{
    height:800px;
  }
  .index-wrap{
    width: 100%;
    display: flex;
  }
  .refresh-list-con {
    border: 1px solid #EBEEF5;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    display: inline-block;
    vertical-align: middle;
    width:16%;
    height:990px;
    padding: 20px;
    box-sizing: border-box;
    flex-shrink: 0;
  }

  .item-con{
    width: 254px;
  }
  .item-con .item {
    width: 254px;
    height: 30px;
    margin-bottom: 10px;
    line-height: 30px;
    font-size: 14px;
    color: #333;
    overflow: hidden;
  }
  .item-con .item:hover{
    color:#409EFF;
    cursor:pointer;
  }
  .checked{
    color:#409EFF!important;
  }
  .index-content{
    width: 1600px;
    height: 90%;
    padding: 0 20px;
    box-sizing: border-box;
  }
  .pagination-comp{
    margin-top: 50px;
    display: flex;
    justify-content: center;
  }
  .el-select .el-input {
    width: 130px;
  }
  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }
  .logout{
    width: 50px;
    height: 26px;
    text-align: center;
    background: #ccc;
    border-radius: 4px;
    line-height: 26px;
    font-size: 14px;
    position: fixed;
    top: 10px;
    right: 20px;
    cursor: pointer;

  }
</style>
