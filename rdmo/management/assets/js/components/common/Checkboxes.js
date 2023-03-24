import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isNil from 'lodash/isNil'

const Checkbox = ({ label, value, onChange }) => (
  <span className="checkbox">
    <label>
        <input type="checkbox" checked={value} onChange={() => onChange(!value)} />
        { label }
    </label>
  </span>
)

Checkbox.propTypes = {
  value: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired
}

export { Checkbox }
