import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const AdditionalTextInput = ({ className, inputValue, disabled, onChange }) => {
  return (
    <input
      type="text"
      className={classNames('form-control input-sm', className)}
      disabled={disabled}
      aria-label={gettext('Additional input')}
      value={inputValue}
      onChange={(event) => onChange(event.target.value)}
    />
  )
}

AdditionalTextInput.propTypes = {
  className: PropTypes.string,
  inputValue: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func.isRequired
}

export default AdditionalTextInput
