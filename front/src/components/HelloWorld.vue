<template>
<div class="container">
  <div class="header-wrap">
    <span class="header-sys-text">{{ $t('headerText.system') }}</span>
    <div class="header-r-wrap">
      <el-dropdown size="small" split-button type="primary" @command="changeLang">
       {{ $t('language.name') }}     
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="cn">{{ $t('language.china') }}</el-dropdown-item>
          <el-dropdown-item command="en">{{ $t('language.english') }}</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
      <!-- <div class="language" v-if="language" @click="changeLang('cn')">{{ $t('language.name') }}</div>
      <div class="language l1" v-else  @click="changeLang('en')">{{ $t('language.name') }}</div> -->
      <div class="logout" @click="outlogFn">{{ $t('loginStatus.login') }}</div>
    </div>
  </div>
  <el-tabs style="margin-top: 70px" v-model="activeName" @tab-click="handleClick">
    <el-tab-pane :label="$t('tabText.index')" name="1">
      <div class="index-wrap">
        <div class="refresh-list-con">
          <el-input :placeholder="$t('inputText.text')" v-model="searchData" clearable class="input-with-select" style="margin-bottom: 20px;">
            <el-button slot="append" icon="el-icon-search" :disabled="searchData == ''? true : false"  @click="getSearchData" :loading="searchLoading"></el-button>
          </el-input>
          <refresh-list @on-bottom="onBotttom">
            <div v-for="(item, index) in leftPageData" :key="index" class="item-con">
              <div :class="[curLeftData === item ? 'item checked': 'item']" @click="getCheckedData(item)">{{item}}</div>
            </div>
          </refresh-list>
        </div>
        <div class="data-list-con">
          <div class="index-content">
            <el-table :data="rightPageData">
              <el-table-column 
                :fixed="index===1" 
                v-for="(item, index) in tableHeader" 
                :key="index" 
                :prop="item.prop" 
                :label="item.label" 
                width="160">
              </el-table-column>
              <el-table-column
                fixed="right"
                label="操作"
                width="160" >
                    <template slot-scope="scope">
                      <el-button slot="reference" type="text" size="small" @click="handleClickZzDetail(scope.row)">职责范围</el-button>
                      <el-button slot="reference" type="text" size="small" @click="handleClickRzDetail(scope.row)">任职要求</el-button>
                    </template>
              </el-table-column>
            </el-table>
          </div>
          <div class="split-page">
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
      </div>
    </el-tab-pane>
    <el-tab-pane  :label="$t('tabText.country')" name="2">
      <el-tabs :tab-position="tabPosition" class="el-tabs-box" @tab-click="handleCountryMap">
        <el-tab-pane v-for="(item, index) in allCountry" :label="item" :key="index" :name="item">
          <div v-if="activeName==2 && item==country"><HtmlPanel :mapSrc="mapSrc" :mapData="mapData" :tableHead="tableHead" /></div>
        </el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane :label="$t('tabText.provence')" name="3" >
      <el-tabs :tab-position="tabPosition" class="el-tabs-box" @tab-click="handleProviceMap">
        <el-tab-pane v-for="(item, index) in allProvince" :label="item" :key="index" :name="item">
          <div v-if="activeName==3 && item==province">
            <HtmlPanel :mapSrc="mapSrc" :mapData="mapData" :tableHead="tableHead"/>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane :label="$t('tabText.city')" name="4">
      <div v-if="activeName==4"><HtmlPanel :mapSrc="mapSrc"  :mapData="mapData" :tableHead="tableHead"/></div>
    </el-tab-pane>
    <el-tab-pane :label="$t('tabText.up')" name="5">
      <!-- <div v-if="activeName==5"><HtmlPanel :mapSrc="mapSrc"/></div> -->
      <div>Coding ...... Please wait ......</div>
    </el-tab-pane>
    <el-tab-pane :label="$t('tabText.down')" name="6">
      <!-- <div v-if="activeName==6"><HtmlPanel :mapSrc="mapSrc"/></div> -->
      <div>Coding ...... Please wait ......</div>
    </el-tab-pane>
    <el-tab-pane :label="$t('tabText.require')" name="7">
      <!-- <div v-if="activeName==6"><HtmlPanel :mapSrc="mapSrc"/></div> -->
      <div>Coding ...... Please wait ......</div>
    </el-tab-pane>
  </el-tabs>
</div>
</template>
<script>
import HtmlPanel from "./HtmlPanel.vue";  // 根据实际路径导入
import RefreshList from "./RefreshList.vue";
  export default {
    components:{
      HtmlPanel,
      RefreshList
    },
    data() {
      return {
        language: true, // true 英文 false  中文
        activeName: '1',
        tabPosition: 'left',
        allProvince:[],
        province:'上海市',
        allCountry: [],
        country: '',
        loading: false,
        searchData: '',
        searchLoading: false,
        leftPageData:[],
        leftTotal:0,
        leftPageNum: 1,
        leftPageLimt: 30,
        curLeftData:'',
        rightPageData:[],
        rightTotal:0,
        rightPageNum: 1,
        rightPageLimt: 10,
        mapSrc:'',
        tableHeader:[],
        // tableHeader:[{
        //   prop:"股票代码",
        //   label:"股票代码"
        // },{
        //   prop:"雇主名称",
        //   label:"雇主名称"
        // },{
        //   prop:"职位名称",
        //   label:"职位名称"
        // },{
        //   prop:"薪资范围",
        //   label:"薪资范围"
        // },{
        //   prop:"年薪下限",
        //   label:"年薪下限"
        // },{
        //   prop:"年薪上限",
        //   label:"年薪上限"
        // },{
        //   prop:"工作经验要求",
        //   label:"工作经验要求"
        // },{
        //   prop:"工作地点",
        //   label:"工作地点"
        // },{
        //   prop:"学历要求",
        //   label:"学历要求"
        // },{
        //   prop:"发布日期",
        //   label:"发布日期"
        // },{
        //   prop:"语言要求",
        //   label:"语言要求"
        // },{
        //   prop:"年龄要求",
        //   label:"年龄要求"
        // },{
        //   prop:"雇主所在行业",
        //   label:"雇主所在行业"
        // }],
        visible: false,
        mapData: [],
        tableHead: []
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
          this.mapSrc=`https://xray-lab.space/dashboard/resource/get_map_by_country/${this.country}?time=${new Date().getTime()}`
          this.getMapData()
        } else if(newval == 3){
          this.mapSrc=`https://xray-lab.space/dashboard/resource/get_map_by_province/${this.province}`
          this.getProviceMapData(this.province)
        }else if(newval == 4){
          this.mapSrc="https://xray-lab.space/dashboard/resource/get_map_of_top_city"
          this.getOneMapData()  
        }else if(newval == 5){
          this.mapSrc="https://xray-lab.space/dashboard/resource/get_map_of_top_rise"
        }else if(newval == 6){
          this.mapSrc="https://xray-lab.space/dashboard/resource/get_map_of_tail_reduce"
        }else if(newval == 7){
          this.mapSrc="https://xray-lab.space/dashboard/resource/get_map_of_tail_reduce"
        }
      } 
    },
    created(){
      this.indexLeftData(this.leftPageNum, this.leftPageLimt)   
      if(window.localStorage.getItem('user_lang') == null){
        localStorage.setItem("user_lang", "cn")
      }                         
},
    mounted(){
      this.getAllProvince(),
      this.getAllCountry()
      this.getHead()
    },
    methods: {
      getHead(){
        this.tableHeader = []
        this.tableHeader = this.tableHeader.concat([{
          prop:"股票代码",
          label: this.$t('tableHead.StockCode')
        },{
          prop:"雇主名称",
          label: this.$t('tableHead.employerName')
        },{
          prop:"职位名称",
          label: this.$t('tableHead.JobTitle')
        },{
          prop:"薪资范围",
          label: this.$t('tableHead.salaryRange')
        },{
          prop:"年薪下限",
          label: this.$t('tableHead.LowerLimitOfAnnualSalary')
        },{
          prop:"年薪上限",
          label: this.$t('tableHead.AnnualSalaryCeiling')
        },{
          prop:"工作经验要求",
          label: this.$t('tableHead.WorkExperienceRequirements')
        },{
          prop:"工作地点",
          label: this.$t('tableHead.WorkLocation')
        },{
          prop:"学历要求",
          label: this.$t('tableHead.EducationalRequirements')
        },{
          prop:"发布日期",
          label: this.$t('tableHead.ReleaseDate')
        },{
          prop:"语言要求",
          label: this.$t('tableHead.salaryRange')
        },{
          prop:"年龄要求",
          label: this.$t('tableHead.LanguageRequirements')
        },{
          prop:"雇主所在行业",
          label: this.$t('tableHead.AgeRequirements')
        }])
      },
      changeLang(lang){
        if(lang === 'cn') {
          this.language = false
        } else {
          this.language = true
        }

        this.$i18n.locale = lang; //关键语句
        localStorage.setItem("user_lang", lang);
        this.getHead()
      },
      // handleCommand(command) {
      //   this.$message('click on item ' + command);
      // },
      handleClick(tab, event) {
        console.log(tab, event);
      },
      // 首页左侧数据
      indexLeftData(num,limt){
        this.$http.get(`/resource/get_employer_by_limit/${num}/${limt}`).then(res=>{
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
          this.$http.get(`/resource/get_employer/${this.searchData}`).then(res=>{
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
        this.rightPageLimt = 10
        this.getRightData(item,this.rightPageNum,this.rightPageLimt)
      },
      // 左侧加载
      onBotttom() {
        this.leftPageNum = this.leftPageNum + 1
        this.indexLeftData(this.leftPageNum, this.leftPageLimt)
      },
      // 首页右侧数据
      getRightData(_curLeftData,_rightPageNum,_rightPageLimt){
        this.$http.get(`/resource/get_employer_data_by_limit/${_curLeftData}/${_rightPageNum}/${_rightPageLimt}`).then(res=>{
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
      // 获取省份
      getAllProvince(){
        this.$http.get('/resource/get_all_province').then(res=>{
          this.allProvince = res.data
          this.province = res.data[0]
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      // 获取国家
      getAllCountry(){
        this.$http.get('/resource/get_all_country').then(res=>{
          this.allCountry = res.data
          this.country = res.data[0]
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      handleCountryMap(e){
        this.country = e.name
        this.mapSrc=`https://xray-lab.space/dashboard/resource/get_map_by_country/${this.country}?time=${new Date().getTime()}`
      },
      handleProviceMap(e){
        this.province = e.name
        this.mapSrc=`https://xray-lab.space/dashboard/resource/get_map_by_province/${this.province}`
        this.getProviceMapData(e.name)
      },
      outlogFn(){
        this.$http.post('/user/logout',{
          username: this.$route.query.username
        }).then(res=>{
          if(res.code == 200) this.$router.replace('/')
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      getMapData(){
        this.$http.get('/resource/get_all_province').then(res=>{
          let arr = [{ prop: '时间', label: '时间'}]
          res.data.forEach((item)=>{
            arr.push({ prop: item, label: item })
          })
          this.tableHead = arr
        }).catch(()=>{
          alert('接口错误！')
        })
        this.$http.get('/resource/get_data_by_country/中国').then(res=>{
          this.mapData = res.data
        }).catch(()=>{
          alert('接口错误！')
        })
      },
      getProviceMapData(province){
        this.$http.get(`https://xray-lab.space/dashboard/resource/get_data_by_province/${province}`).then(res=>{
          let arr = []
          Object.keys(res.data[0]).map(key => {
            arr.push({
              prop: key, label: key
            })
          })
          this.tableHead = arr
          this.mapData = res.data
          console.log(this.tableHead ,this.mapData)
        })
      },
      getOneMapData(){
        this.$http.get('https://xray-lab.space/dashboard/resource/get_data_of_top_city').then(res=>{
          let arr = []
          Object.keys(res.data[0]).map(key => {
            arr.push({
              prop: key, label: key
            })
          })
          this.tableHead = arr
          this.mapData = res.data
          console.log(res, 'res')
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
    height: 950px;
    display: flex;
  }
  .refresh-list-con {
    border: 1px solid #EBEEF5;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    display: inline-block;
    vertical-align: middle;
    width:15%;
    height:900px;
    padding: 20px;
    box-sizing: border-box;
    flex-shrink: 0;
  }
  .data-list-con {
    border: 1px solid #EBEEF5;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    display: inline-block;
    vertical-align: middle;
    width:85%;
    height:900px;
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
    height: 800px;
    padding: 0 20px;
    box-sizing: border-box;
  }
  .split-page{
    width: 1600px;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
    padding: 0 20px;
    box-sizing: border-box;
  }
  .pagination-comp{
    /* margin-top: 50px; */
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
    width: 80px;
    height: 32px;
    text-align: center;
    background: #ccc;
    border-radius: 4px;
    line-height: 32px;
    font-size: 14px;
    /* position: fixed;
    top: 10px;
    right: 20px; */
    cursor: pointer;
    margin-left: 20px;
  }
  .language{
    width: 80px;
    height: 26px;
    text-align: center;
    background: #409EFF;
    border-radius: 4px;
    line-height: 26px;
    font-size: 14px;
    /* position: fixed;
    top: 10px;
    right: 120px; */
    cursor: pointer;
    color: #fff;
  }
  .header-wrap{
    width: 100%;
    height: 70px;
    padding: 0 20px;
    box-sizing: border-box;
    background: rgb(3, 3, 50);
    color: #fff;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 100;
  }
  .header-sys-text{
    font-size: 20px;
    font-weight: 600;
  }
  .header-r-wrap{
    display: flex;
  }
</style>
