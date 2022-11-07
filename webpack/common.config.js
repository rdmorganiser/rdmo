const webpack = require('webpack')
const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  entry: {
    management: [
      './rdmo/management/assets/js/management.js',
      './rdmo/management/assets/scss/management.scss'
    ]
  },
  resolve: {
    alias: {
      rdmo: path.resolve(__dirname, '../rdmo/')
    },
    extensions: ['*', '.js', '.jsx']
  },
  output: {
    filename: '[name]/static/management/js/[name].js',
    publicPath: '/static/',
    path: path.resolve(__dirname, '../rdmo/'),
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules|bower_components)/,
        loader: "babel-loader",
        options: { presets: ['@babel/env','@babel/preset-react'] }
      },
      {
        test: /\.s?css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name]/static/management/css/[name].css',
      chunkFilename: '[name]/static/management/css/[id].css'
    }),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    })
  ]
}
