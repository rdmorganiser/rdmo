import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty, isNil, uniqueId } from 'lodash'

const Input = ({
  type = 'text',
  className,
  debounce,
  label,
  placeholder,
  help,
  isDisabled,
  errors,
  value,
  inputRef,
  onChange,
  onEnter
}) => {
  const id = uniqueId('input-')

  // store the value in a local state (only when debouncing)
  const [inputValue, setInputValue] = isNil(debounce) ? [value, () => {}] : useState(value)

  // use the debounce hook on the onChange callback (only when debouncing)
  const callOnChange = isNil(debounce) ? (
    (value) => onChange(value)
  ) : useDebouncedCallback((value) => onChange(value), debounce)

  // update the local state if the value prop changes (only when debouncing)
  useEffect(() => setInputValue(value), [value])

  const handleChange = (event) => {
    const value = event.target.value

    setInputValue(value)  // will update the local state (only when debouncing)
    callOnChange(value)   // will call onChange (with or without debouncing)
  }

  return (
    <div className={classNames('form-group', className)}>
      <label className="form-label" htmlFor={id}>{label}</label>
      <input
        ref={inputRef}
        id={id}
        type={type}
        className={
          classNames('form-control', {
            'is-invalid': !isEmpty(errors)
          })
        }
        placeholder={placeholder}
        disabled={isDisabled}
        value={inputValue}
        onChange={handleChange}
        onKeyPress={
          (event) => {
            if (!isNil(onEnter) && event.code === 'Enter') {
              onEnter(event.target.value)
            }
          }
        }
      />
      {
        errors && (
          <div className="invalid-feedback">
            {errors.map((error, index) => <div key={index}>{error}</div>)}
          </div>
        )
      }
      {
        help && <div className="form-text">{help}</div>
      }
    </div>
  )
}

Input.propTypes = {
  type: PropTypes.string,
  className: PropTypes.string,
  debounce: PropTypes.number,
  label: PropTypes.string,
  placeholder: PropTypes.string,
  help: PropTypes.oneOfType([PropTypes.node, PropTypes.string]),
  isDisabled: PropTypes.bool,
  errors: PropTypes.array,
  value: PropTypes.string.isRequired,
  inputRef: PropTypes.object,
  onChange: PropTypes.func.isRequired,
  onEnter: PropTypes.func
}

export default Input
