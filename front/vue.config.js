const { defineConfig } = require('@vue/cli-service')


module.exports = defineConfig({
  // publicPath: process.env.NODE_ENV === "production" ? "/dashboard/" : "/",
  publicPath: '/',
  transpileDependencies: true,
  lintOnSave: false,
  css: {
    extract: {
        filename: 'dashboard/css/[name].css',
        chunkFilename:  'dashboard/css/[name].css'
    },
  },

  chainWebpack: (config) => {

    // js file
    config.output
      .filename('dashboard/js/[name].js')
      .chunkFilename('dashboard/js/[name].js');

    config.module
      .rule('fonts')
      .test(/\.(woff2?|eot|ttf|otf)(\?.*)?$/i)
      .type('asset')
      .set("generator", {
        'filename': 'dashboard/fonts/[name][ext]',
      });

    config.module
      .rule("svg")
      .test(/\.(svg)(\?.*)?$/)
      .set("type", "asset/resource")
      .set("generator", {
        'filename': 'dashboard/svg/[name][ext]',
      });

    config.module
      .rule("images")
      .test(/\.(png|jpe?g|gif|webp|avif)(\?.*)?$/)
      .set("type", "asset")
      .set("generator", {
        'filename': 'dashboard/img/[name][ext]',
      });

    config.module
      .rule("media")
      .test(/\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/)
      .set("type", "asset")
      .set("generator", {
        'filename': 'dashboard/media/[name][ext]',
      });
  },

  devServer: {
    open: true,
    historyApiFallback: true,
    allowedHosts: "all",
    host: '0.0.0.0',
    port: 58080,
    https: false,
    proxy: null,
    hot: false,
    client: {
      webSocketURL: 'wss://sfi.cuhk.edu.cn:443/dashboard/wss',
    },
    headers: {
      'Access-Control-Allow-Origin': '*',
    }
  }
})
