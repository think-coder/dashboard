const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  // publicPath: '/',
  publicPath: process.env.NODE_ENV === "production" ? "/dashboard/" : "/",
  devServer: {
    historyApiFallback: true,
    allowedHosts: "all",
  }
})
