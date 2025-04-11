import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { get, isNil } from 'lodash'

const AdditionalTextInput = ({ className, value, option, disabled, onChange }) => {
  const [inputValue, setInputValue] = useState('')

  useEffect(() => {
    if (isNil(value)) {
      setInputValue('')
    } else {
      setInputValue(value.option == option.id ? value.text : '')
    }
  }, [get(value, 'id'), get(value, 'text'), get(value, 'option'), get(value, 'external_id')])

  return (
    <span className={className}>
      <input
        type="text"
        className="form-control input-sm"
        disabled={disabled}
        aria-label={gettext('Additional input')}
        value={inputValue}
        onChange={(event) => {
          setInputValue(event.target.value)
          onChange(value, option, event.target.value)
        }}
      />
    </span>
  )
}

AdditionalTextInput.propTypes = {
  className: PropTypes.string,
  value: PropTypes.object,
  option: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  onChange: PropTypes.func.isRequired
}

export default AdditionalTextInput
