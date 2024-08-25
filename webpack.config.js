const webpack = require('webpack')
const { merge } = require('webpack-merge')
const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const TerserPlugin = require('terser-webpack-plugin')

// list of separate config objects for each django app and their corresponding java script applications
const configList = [
  {
    name: 'core',
    entry: {
      base: [
        './rdmo/core/assets/js/base.js',
        './rdmo/core/assets/scss/base.scss'
      ],
      'base-bs53': [
        './rdmo/core/assets/js/_bs53/base.js',
        './rdmo/core/assets/scss/_bs53/base.scss'
      ]
    },
    output: {
      path: path.resolve(__dirname, './rdmo/core/static/core/'),
    }
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
      projects: [
        './rdmo/projects/assets/js/projects.js',
        './rdmo/projects/assets/scss/projects.scss'
      ],
      project: [
        './rdmo/projects/assets/js/project.js',
        './rdmo/projects/assets/scss/project.scss'
      ]
    },
    output: {
      path: path.resolve(__dirname, './rdmo/projects/static/projects/'),
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
        test: /(fonts|files)[\\/].*\.(svg|woff2?|ttf|eot|otf)(\?.*)?$/,
        loader: 'file-loader',
        type: 'javascript/auto',
        options: {
          name: '[name].[ext]',
          outputPath: 'fonts',
          postTransformPublicPath: (p) => `'../' + ${p}`,
          esModule: false,
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

// combine config depending on the provided --mode command line option
module.exports = (env, argv) => {
  return configList.map(config => {
    if (argv.mode === 'development') {
      return merge(config, baseConfig, developmentConfig)
    } else {
      return merge(config, baseConfig, productionConfig)
    }
  })
}
