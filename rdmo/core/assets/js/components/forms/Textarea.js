import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, isNil, uniqueId } from 'lodash'

import { useDebouncedCallback } from 'use-debounce'

const Textarea = ({ rows, className, debounce, label, placeholder, help, isDisabled, errors, value, onChange }) => {
  const id = uniqueId('textarea-')

  // store the value in a local state (only when debouncing)
  const [textareaValue, setTextareaValue] = isNil(debounce) ? [value, () => {}] : useState(value)

  // use the debounce hook on the onChange callback (only when debouncing)
  const callOnChange = isNil(debounce) ? (value) => onChange(value)
                                       : useDebouncedCallback((value) => onChange(value), debounce)

  // update the local state if the value prop changes (only when debouncing)
  useEffect(() => setTextareaValue(value), [value])

  const handleChange = (event) => {
    const value = event.target.value

    setTextareaValue(value)  // will update the local state (only when debouncing)
    callOnChange(value)      // will call onChange (with or without debouncing)
  }

  return (
    <div className={classNames('form-group', className)}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <textarea
        rows={rows}
        id={id}
        className={classNames('form-control', {
          'is-invalid': !isEmpty(errors)
        })}
        placeholder={placeholder}
        disabled={isDisabled}
        value={textareaValue}
        onChange={handleChange}
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

Textarea.propTypes = {
  rows: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  className: PropTypes.string,
  debounce: PropTypes.number,
  label: PropTypes.string,
  placeholder: PropTypes.string,
  help: PropTypes.string,
  isDisabled: PropTypes.bool,
  errors: PropTypes.array,
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired
}

export default Textarea
