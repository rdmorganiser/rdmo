import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'

import { useDebouncedCallback } from 'use-debounce'

import Input from './Input'

const InputDebounced = ({ value, onChange, ...props }) => {

  const [inputValue, setInputValue] = useState('')

  useEffect(() => setInputValue(value), [value])

  const debouncedOnChange = useDebouncedCallback((value) => onChange(value), 500)

  return (
    <Input {...props}
      value={inputValue}
      onChange={(value) => {
        setInputValue(value)
        debouncedOnChange(value)
      }}
    />
  )
}

InputDebounced.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired
}

export default InputDebounced
