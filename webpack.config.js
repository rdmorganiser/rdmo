const webpack = require('webpack')
const { merge } = require('webpack-merge')
const path = require('path')
const CopyPlugin = require('copy-webpack-plugin')
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
      ]
    },
    output: {
      path: path.resolve(__dirname, './rdmo/core/static/core/'),
    },
    plugins: [
      new CopyPlugin({
        patterns: [
          {
            from: '**/*',
            to: './/fonts/',
            context: './rdmo/core/assets/fonts/'
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
      projects: [
        './rdmo/projects/assets/js/projects.js',
        './rdmo/projects/assets/scss/projects.scss'
      ],
      interview: [
        './rdmo/projects/assets/js/interview.js',
        './rdmo/projects/assets/scss/interview.scss'
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
          {
            loader: 'sass-loader',
            options: {
              implementation: require('sass'), // Explicitly use Dart Sass
              warnRuleAsWarning: true, // Treat `@warn` as warnings, not errors
              sassOptions: {
                // https://sass-lang.com/documentation/breaking-changes/import/#can-i-silence-the-warnings
                silenceDeprecations: ['import'],
                quietDeps: true,
                verbose: false,
              },
            },
          },
        ],
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
  bail: true, // Stop the build on errors
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    })
  ],
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()]
  },
}

const ignorePerformanceWarnings = {
  performance: {
    hints: false, // Suppress performance warnings in prod
    maxAssetSize: 1024000, // 🔹 Set asset size limit (1MB per file)
    maxEntrypointSize: 2048000, // 🔹 Set entrypoint size limit (2MB)
  },
}

// combine config depending on the provided --mode command line option
module.exports = (env, argv) => {
  return configList.map(config => {
    switch (argv.mode) {

      case 'development':
        // used for build and watch
        return merge(config, baseConfig, developmentConfig)

      case 'production':
        if (env && env['ignore-perf']) {
          // build:dist will ignore performance warnings but fails on other warnings
          return merge(config, baseConfig, productionConfig, ignorePerformanceWarnings)
        }
        // build:prod
        return merge(config, baseConfig, productionConfig)

      default:
        throw new Error('Invalid mode')
    }
  })
}
