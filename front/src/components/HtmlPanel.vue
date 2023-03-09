<template>
  <iframe
   name="iframeMap"
   id="iframeMapViewComponent"
   width="100%"
   height="470px"
   :src="`http://106.52.123.19:58000/dashboard/get_map_by_country/${data}`"
   frameborder="0"
   scrolling="no"
   ref="iframeDom"
  ></iframe>
</template>
<script>
export default {
props: ["data"],
  data() {
    return {
      mounted(){
        console.log(this.data, 'data')
      }
    }
  }
};
</script>