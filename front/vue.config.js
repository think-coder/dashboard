const { defineConfig } = require('@vue/cli-service')
const path = require('path')
const fs = require('fs')

module.exports = defineConfig({
  // publicPath: './dashboard',
  transpileDependencies: true,
  lintOnSave: false,
  // outputDir: './',
  configureWebpack: (config) => {
    config.output.filename = 'dashboard/[name].js';
    config.output.chunkFilename = 'dashboard/[name].js';
  },
  // publicPath: '/',
  publicPath: process.env.NODE_ENV === "production" ? "/dashboard/" : "/",
  devServer: {
    open: true,
    historyApiFallback: true,
    allowedHosts: "all",
    host: '0.0.0.0',
    port:58080,
    client: {
      webSocketURL: 'wss://sfi.cuhk.edu.cn:443/dashboard/wss',
    },
    headers: {
      'Access-Control-Allow-Origin': '*',
    }
  }
})
