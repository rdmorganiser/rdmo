import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { get, isNil } from 'lodash'

const AdditionalTextInput = ({ value, option, disabled, onChange }) => {
  const [inputValue, setInputValue] = useState('')

  useEffect(() => {
    if (isNil(value)) {
      setInputValue('')
    } else {
      setInputValue(value.option == option.id ? value.text : '')
    }
  }, [get(value, 'id'), get(value, 'option')])

  return (
    <input
      type="text"
      className="form-control input-sm"
      disabled={disabled}
      value={inputValue}
      onChange={(event) => {
        setInputValue(event.target.value)
        onChange(value, option, event.target.value)
      }}
    />
  )
}

AdditionalTextInput.propTypes = {
  value: PropTypes.object,
  option: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  onChange: PropTypes.func.isRequired
}

export default AdditionalTextInput
