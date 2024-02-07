const webpack = require('webpack')
const { merge } = require('webpack-merge')

const commonConfig = require('./common.config.js')

module.exports = commonConfig.map(common => {
  return merge(common, {
    devtool: 'eval',
    plugins: [
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify('development')
      })
    ]
  })
})
