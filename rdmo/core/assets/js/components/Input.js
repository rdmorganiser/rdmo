import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, uniqueId } from 'lodash'

const Input = ({ type = 'text', className, label, placeholder, help, disabled, errors, value, onChange }) => {
  const id = uniqueId('input-')

  return (
    <div className={classNames('form-group', className)}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <input
        id={id}
        type={type}
        className={classNames('form-control', {
          'is-invalid': !isEmpty(errors)
        })}
        placeholder={placeholder}
        disabled={disabled}
        value={value}
        onChange={event => onChange(event.target.value)}
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
  label: PropTypes.string,
  placeholder: PropTypes.string,
  help: PropTypes.string,
  disabled: PropTypes.bool,
  errors: PropTypes.array,
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired
}

export default Input
