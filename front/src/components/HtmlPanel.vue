<template>
  <div>
    <iframe
    name="iframeMap"
    id="iframeMapViewComponent"
    width="100%"
    height="700px"
    :src="mapSrc"
    frameborder="0"
    scrolling="no"
    ref="iframeDom"
    ></iframe>
    <div style="width: 100%">
      <el-table :data="mapData">
        <el-table-column 
          v-for="(item, index) in tableHead" 
          :key="index" 
          :prop="item.prop" 
          :label="item.label" 
          width="160">
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
export default {
  props: ["mapSrc", "mapData", "tableHead"],
  data() {
    return {

    }
  }
};
</script>

<style scope>
 .el-tabs-box{
    height:100%!important;
  }
  .el-tabs--to{
    height: 100%;
  }
</style>