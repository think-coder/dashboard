// About.vue
<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="首页" name="1">
       <el-tabs :tab-position="tabPosition" style="height: 200px;">
        <el-tab-pane label="宁德时代">宁德时代</el-tab-pane>
        <el-tab-pane label="平安银行">平安银行</el-tab-pane>
        <el-tab-pane label="万达电影">万达电影</el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane label="全国招聘数据" name="2">全国招聘数据</el-tab-pane>
    <el-tab-pane label="省级招聘数据" name="3">
      <el-tabs :tab-position="tabPosition" style="height: 200px;">
        <el-tab-pane label="山西省">山西省</el-tab-pane>
        <el-tab-pane label="山东省">山东省</el-tab-pane>
        <el-tab-pane label="广东省">广东省</el-tab-pane>
      </el-tabs>
    </el-tab-pane>
    <el-tab-pane label="市级招聘数据" name="4">市级招聘数据</el-tab-pane>
    <el-tab-pane label="一线/新一线" name="5">一线/新一线</el-tab-pane>
    <el-tab-pane label="增长最快" name="6">增长最快</el-tab-pane>
    <el-tab-pane label="下降最快" name="7">下降最快</el-tab-pane>
  </el-tabs>
</template>
<script>
import axios from 'axios'
import { defineComponent, onMounted } from "vue"
export default defineComponent({
  name: "About",
  data() {
    return {
      activeName: "1",
      tabPosition: "left"
    }
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    }
  },
  setup()
  {
    onMounted(
      () => {
        axios({
          method: "get",
          url: "http://172.19.125.144:8001/dashboard/get_total_employer/"
        })
        .then(res => {
          console.log(res.data)
          console.log(res)
        })
        .catch(err => {
          console.log("err")
        })
      }
    )
    let a = 1
    return {
      a
    }
  }
})

</script>
