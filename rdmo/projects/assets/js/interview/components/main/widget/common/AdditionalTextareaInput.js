import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const AdditionalTextareaInput = ({ className, inputValue, disabled, onChange }) => {
  return (
    <textarea
      rows={4}
      className={classNames('form-control input-sm', className)}
      disabled={disabled}
      aria-label={gettext('Additional input')}
      value={inputValue}
      onChange={(event) => onChange(event.target.value)}
    />
  )
}

AdditionalTextareaInput.propTypes = {
  className: PropTypes.string,
  inputValue: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func.isRequired
}

export default AdditionalTextareaInput
