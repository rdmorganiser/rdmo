import React from 'react'
import PropTypes from 'prop-types'

const Checkbox = ({ label, value, onChange }) => (
  <span className="checkbox">
    <label>
        <input type="checkbox" checked={value} onChange={() => onChange(!value)} />
        { label }
    </label>
  </span>
)

Checkbox.propTypes = {
  label: PropTypes.oneOfType([PropTypes.object, PropTypes.string]).isRequired,
  value: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired
}

export { Checkbox }
