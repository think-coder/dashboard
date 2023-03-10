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
              <el-table-column v-for="(item, index) in tableHeader" :key="index" :prop="item.prop" :label="item.label" width="180"></el-table-column>
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
      <div v-if="activeName==2"><HtmlPanel data="中国" /></div>
    </el-tab-pane>
    <el-tab-pane label="省级招聘数据" name="3" >
      <el-tabs :tab-position="tabPosition" class="el-tabs-box" @tab-click="handleProviceMap">
        <el-tab-pane v-for="(item, index) in allProvince" :label="item" :key="index" :name="item">
          <div v-if="activeName==3 && item==province"><HtmlPanel :data="province" /></div>
        </el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane label="一线/新一线" name="5">一线/新一线</el-tab-pane>
    <el-tab-pane label="增长最快" name="6">增长最快</el-tab-pane>
    <el-tab-pane label="下降最快" name="7">下降最快</el-tab-pane>
  </el-tabs>
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
            this.leftPageData = res
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
      },
      
    }
  };
</script>
<style>
  .container{
    width: 100%;
    height: 100vh;
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
</style>
