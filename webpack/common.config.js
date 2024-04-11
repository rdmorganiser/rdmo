const webpack = require('webpack')
const { merge } = require('webpack-merge')
const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const base = {
  resolve: {
    alias: {
      rdmo: path.resolve(__dirname, '../rdmo/')
    },
    extensions: ['*', '.js', '.jsx']
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'css/[name].css',
      chunkFilename: 'css/[id].css'
    }),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    })
  ],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        options: { presets: ['@babel/env','@babel/preset-react'] }
      },
      {
        test: /\.s?css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ]
      },
      {
        test: /\.(svg|woff2?|ttf|eot|otf)$/,
        type: 'javascript/auto',
        include: /fonts/,  // This line ensures only files in the 'fonts' folder are processed
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
          outputPath: 'fonts/',  // Output directory for the fonts within the output path of webpack
          publicPath: '../fonts/',  // Sets correct public path to reference fonts in the CSS
          esModule: false,
        }
      }
    ]
  }
}

module.exports = [
  merge(base, {
    name: 'management',
    entry: {
      management: [
        './rdmo/management/assets/js/management.js',
        './rdmo/management/assets/scss/management.scss'
      ]
    },
    output: {
      filename: 'js/management.js',
      path: path.resolve(__dirname, '../rdmo/management/static/management/'),
    }
  })
]
