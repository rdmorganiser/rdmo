module.exports = {
  "globals": {
    "gettext": true,
    "ngettext": true,
    "interpolate": true,
    "process": true,
    "require": true
  },
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended"
  ],
  "overrides": [],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "plugins": [
    "react"
  ],
  "rules": {
    "indent": "off",
    "no-empty-pattern": "off",
    "linebreak-style": [
      "error",
      "unix"
    ],
    "quotes": [
      "error",
      "single"
    ],
    "semi": [
      "error",
      "never"
    ]
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
