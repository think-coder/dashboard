<template>
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
</template>
<script>
export default {
  props: ["mapSrc"],
  data() {
    return {
      mounted(){
       
      }
    }
  }
};
</script>