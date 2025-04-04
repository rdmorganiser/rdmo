import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'

import { useDebouncedCallback } from 'use-debounce'

import Textarea from './Textarea'

const TextareaDebounced = ({ value, onChange, ...props }) => {

  const [inputValue, setInputValue] = useState('')

  useEffect(() => setInputValue(value), [value])

  const debouncedOnChange = useDebouncedCallback((value) => onChange(value), 500)

  return (
    <Textarea {...props}
      value={inputValue}
      onChange={(value) => {
        setInputValue(value)
        debouncedOnChange(value)
      }}
    />
  )
}

TextareaDebounced.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired
}

export default TextareaDebounced
