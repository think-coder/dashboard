<template>
  <div
    class="list-warp-template"
    @touchstart="handlerStart"
    @touchend="handlerEnd"
    @touchmove="handlerMove"
    @scroll="handlerScroll"
    ref="listWrapRef"
  >
    <div class="top-refresh" :style="{ height: refresh.height + 'px' }">
      <div v-show="refresh.height > 30">
        {{ refreshLoading ? "刷新中" : "松开刷新" }}
      </div>
    </div>
    <div class="main-list">
      <slot></slot>
    </div>
    <div class="bottom-loading" v-show="bottomLoading">加载中</div>
  </div>
</template>
<script>
let timer = null;
export default {
  name: "RefreshList",
  props: {
    refreshLoading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      position: 0,
      startInit: 0,
      bottomLoading: false,
      refresh: {
        height: 0,
      },
    };
  },
  created() {},
  watch: {
    refreshLoading(val) {
      if (!val) {
        this.refresh.height = 0;
      }
    },
  },
  computed: {},
  mounted() {},
  methods: {
    handlerScroll(e) {
      const eDom = e.target;
      const scrollTop = e.target.scrollTop;
      // 判断是否到底了
      let scrollPosition = eDom.scrollHeight - e.target.offsetHeight;
      if (timer) {
        clearTimeout(timer);
      }

      timer = setTimeout(() => {
        this.bottomLoading = true;
        if (scrollPosition <= scrollTop) {
          this.$emit("on-bottom"); //到底了
        }
      }, 200);
      this.position = scrollTop;
      // 滚动事件，返回当前滚动位置
      this.$emit("on-scroll", scrollPosition);
    },
    // 返回顶部
    handlerBackTop() {
      const dom = this.$refs.listWrapRef;
      dom.scrollTop = 0;
    },
    // 触摸开始
    handlerStart(e) {
      this.startInit = parseInt(e.touches[0].clientY);
    },
    // 滑动中,下拉
    handlerMove(e) {
      if (this.position === 0 && !this.refreshLoading) {
        const Y = parseInt(e.touches[0].clientY);
        const range = Y - this.startInit;
        this.refresh.height = range;
      }
    },
    // 滑动结束
    handlerEnd() {
      if (this.refresh.height >= 30) {
        this.refresh.height = 40;
        this.$emit("on-refresh");
        this.$emit("update:refreshLoading", true);
      } else {
        this.refresh.height = 0;
      }
      this.startInit = 0;
    },
  },
};
</script>

<style >
.list-warp-template {
  display: block;
  /* height: 100vh; */
  height: 100%;
  overflow-y: auto;
}
.top-refresh {
  background-color: #ccc;
  height: 0;
  width: 100%;
  transition: height 0.1s linear;
  overflow: hidden;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-list {
  width: 100%;
}

.bottom-loading {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  width: 100%;
  background-color: #f0f0f0;
}
</style>