const webpack = require('webpack')
const { merge } = require('webpack-merge')
const TerserPlugin = require('terser-webpack-plugin')

const commonConfig = require('./common.config.js')

module.exports = commonConfig.map(common => {
  return merge(common, {
    plugins: [
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify('production')
      })
    ],
    optimization: {
      minimize: true,
      minimizer: [new TerserPlugin()]
    }
  })
})
