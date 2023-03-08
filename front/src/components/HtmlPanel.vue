<template>
  <div id='htmlData'></div>
  <!-- <iframe :src="htmlData"></iframe> -->
</template>
<script>
export default {
props: {},
  data() {
    return {
      htmlData: "",
    }
  },
  mounted() {
    this.load();
    
  },
  methods: {
    
    load() {
        let param = {accept: "text/html, text/plain"};
        this.$http.get('/dashboard/get_map_by_country/china', param).then(res => { 
          // const htmlData = document.getElementById('htmlData')
          document.write(res);
          document.close();

          // this.htmlData = res
          
          // this._nexttick()
        })
    },
  }
};
</script>