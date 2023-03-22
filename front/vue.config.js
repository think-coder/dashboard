const { defineConfig } = require('@vue/cli-service')
const path = require('path')
const fs = require('fs')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  // publicPath: '/',
  publicPath: process.env.NODE_ENV === "production" ? "/dashboard/" : "/",
  devServer: {
    historyApiFallback: true,
    allowedHosts: "all",
    // open: true,
    // https: {
    //   cert: fs.readFileSync(path.join(__dirname, 'src/ssl/cert.crt')),
    //   key: fs.readFileSync(path.join(__dirname, 'src/ssl/cert.key'))
    // }
  }
})
