import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { useDebouncedCallback } from 'use-debounce'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

const RangeInput = ({ value, minimum, maximum, step, disabled, isDefault, updateValue }) => {
  const [inputValue, setInputValue] = useState('')
  useEffect(() => {setInputValue(value.text)}, [value.id])

  const handleChange = useDebouncedCallback((value, text) => {
    updateValue(value, { text })
  }, 500)

  const classnames = classNames({
    'range': true,
    'default': isDefault
  })

  return (
    <div className={classnames}>
      <span className="badge">{inputValue}</span>
      <input
        type="range"
        min={isEmpty(minimum) ? '0' : minimum}
        max={isEmpty(maximum) ? '100' : maximum}
        step={isEmpty(step) ? '1' : step}
        disabled={disabled}
        value={inputValue}
        onChange={(event) => {
          setInputValue(event.target.value)
          handleChange(value, event.target.value)
        }}
      />
    </div>
  )
}

RangeInput.propTypes = {
  value: PropTypes.object.isRequired,
  minimum: PropTypes.number,
  maximum: PropTypes.number,
  step: PropTypes.number,
  disabled: PropTypes.bool,
  isDefault: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

export default RangeInput
