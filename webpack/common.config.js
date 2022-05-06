const webpack = require('webpack')
const path = require('path');

module.exports = {
  entry: {
    management: './rdmo/management/assets/js/management.js'
  },
  resolve: {
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
      }
    ]
  }
}
