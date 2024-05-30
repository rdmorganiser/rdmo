const webpack = require('webpack')
const { merge } = require('webpack-merge')
const path = require('path')
const CopyPlugin = require('copy-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const TerserPlugin = require('terser-webpack-plugin')

// list of seperate config objects for each django app and their corresponding java script applications
const configList = [
  {
    name: 'core',
    entry: {
      base: [
        './rdmo/core/assets/js/base.js',
        './rdmo/core/assets/scss/base.scss'
      ]
    },
    output: {
      path: path.resolve(__dirname, './rdmo/core/static/core/dist/'),
    },
    plugins: [
      new CopyPlugin({
        patterns: [
          {
            from: 'img/*',
            context: './rdmo/core/assets',
          }
        ]
      })
    ]
  },
  {
    name: 'management',
    entry: {
      management: [
        './rdmo/management/assets/js/management.js',
        './rdmo/management/assets/scss/management.scss'
      ]
    },
    output: {
      path: path.resolve(__dirname, './rdmo/management/static/management/'),
    }
  },
  {
    name: 'projects',
    entry: {
      interview: [
        './rdmo/projects/assets/js/interview.js',
        './rdmo/projects/assets/scss/interview.scss'
      ]
    },
    output: {
      path: path.resolve(__dirname, './rdmo/projects/static/projects/dist/'),
    }
  }
]

// base config for all endpoints
const baseConfig = {
  resolve: {
    alias: {
      rdmo: path.resolve(__dirname, './rdmo/')
    },
    extensions: ['*', '.js', '.jsx']
  },
  output: {
    filename: 'js/[name].js'
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
        test: /(fonts|files)\/.*\.(svg|woff2?|ttf|eot|otf)(\?.*)?$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
          outputPath: 'fonts',
          postTransformPublicPath: (p) => `'../' + ${p}`
        }
      }
    ]
  }
}

// special config for development
const developmentConfig = {
  devtool: 'eval',
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('development')
    })
  ]
}

// special config for production
const productionConfig = {
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    })
  ],
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()]
  }
}

// combine config depending on the provided --mode arg
module.exports = (env, argv) => {
  return configList.map(config => {
    if (argv.mode === 'development') {
      return merge(config, baseConfig, developmentConfig)
    } else {
      return merge(config, baseConfig, productionConfig)
    }
  })
}
