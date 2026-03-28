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
    'simple-import-sort',
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
    'indent': ['error', 2, {
      'SwitchCase': 1,
    }],

    // Enforce spaces around =, +, ==, ?, :, etc.
    'space-infix-ops': 'error',

    // Enforce separate const declarations
    'one-var': ['error', 'never'],

    // Import order
    'simple-import-sort/imports': ['error', {
      groups: [
        // external imports in the given order
        ['^react$', '^prop-types$', '^react', '^[a-z]', '^lodash'],
        // rdmo imports: lowercase first, then capitalized components
        ['^rdmo/.*\\/[a-z]'],
        ['^rdmo/.*\\/[A-Z]'],
        // parent imports: lowercase first, then capitalized components
        ['^\\.\\..*\\/[a-z]'],
        ['^\\.\\..*\\/[A-Z]'],
        // sibling imports: lowercase first, then capitalized  components
        ['^\\./.*\\/[a-z]'],
        ['^\\./.*\\/[A-Z]'],
      ],
    }],

    // Export order
    'simple-import-sort/exports': 'error',

    // Disallow newlines between the operands of a ternary expression
    'multiline-ternary': ['error', 'never'],

    // Ensure spaces after commas
    'comma-spacing': ['error', { before: false, after: true }],

    // Ensure correct multiline imports
    'object-curly-newline': ['error', {
      ImportDeclaration: {
        multiline: true,
        consistent: true
      }
    }],

    // JSX: require a newline before the first prop when the JSX spans multiple lines and there is more than one prop
    'react/jsx-first-prop-new-line': ['error', 'multiline-multiprop'],

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
