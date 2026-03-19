module.exports = {
  'root': true,
  'globals': {
    'gettext': true,
    'ngettext': true,
    'interpolate': true,
    'process': true,
    'require': true
  },
  'env': {
    'browser': true,
    'es2021': true,
    'node': true
  },
  'extends': [
    'eslint:recommended',
    'plugin:react/recommended'
  ],
  'overrides': [],
  'parserOptions': {
    'ecmaVersion': 'latest',
    'sourceType': 'module'
  },
  'plugins': [
    'react'
  ],
  'ignorePatterns': ['**/static/**/*.js'],
  'rules': {
    // Disable unused rules
    'no-empty-pattern': 'off',

    // Unix linebreaks only
    'linebreak-style': ['error', 'unix'],

    // Single quotes, allow double to avoid escaping
    'quotes': [
      'error',
      'single',
      { 'avoidEscape': true }
    ],

    // No semicolons
    'semi': ['error', 'never'],

    // Maximum line length of 120 characters
    'max-len': [
      'error',
      {
        'code': 120,
        'ignoreUrls': true,
        'ignoreRegExpLiterals': true
      }
    ],

    // Indent by 2 spaces
    'indent': [
      'error',
      2,
      {
        'SwitchCase': 1,
        'offsetTernaryExpressions': true
      }
    ],

    // Disallow newlines between the operands of a ternary expression
    'multiline-ternary': ['error', 'never'],

    // JSX: wrap multiline expressions in parens, opening paren on a new line
    'react/jsx-wrap-multilines': [
      'error',
      {
        'declaration': 'parens-new-line',
        'assignment': 'parens-new-line',
        'return': 'parens-new-line',
        'arrow': 'parens-new-line',
        'condition': 'parens-new-line',
        'logical': 'parens-new-line',
        'prop': 'parens-new-line'
      }
    ],

    // JSX curly braces: require newlines inside for multiline expressions
    'react/jsx-curly-newline': [
      'error',
      {
        'multiline': 'require',
        'singleline': 'consistent'
      }
    ],

    // JSX curly brace spacing: no spaces inside { }
    'react/jsx-curly-spacing': [
      'error',
      {
        'when': 'never',
        'children': true
      }
    ],

    // JSX double quotes for props
    'jsx-quotes': ['error', 'prefer-double'],
  },
  'settings': {
    'react': {
      'version': 'detect'
    }
  },
}
