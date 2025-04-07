import React from 'react'
import PropTypes from 'prop-types'

const Checkbox = ({ label, value, onChange }) => {
  const checked = [true, 'true'].includes(value)  // values are stored as string in the local storage

  return (
    <span className="checkbox">
      <label>
          <input type="checkbox" checked={checked} onChange={() => onChange(!checked)} />
          { label }
      </label>
    </span>
  )
}

Checkbox.propTypes = {
  label: PropTypes.oneOfType([PropTypes.object, PropTypes.string]).isRequired,
  value: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]).isRequired,
  onChange: PropTypes.func.isRequired
}

export { Checkbox }
