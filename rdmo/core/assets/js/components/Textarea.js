import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, uniqueId } from 'lodash'

const Textarea = ({ rows, className, label, placeholder, help, disabled, errors, value, onChange }) => {
  const id = uniqueId('textarea-')

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

Textarea.propTypes = {
  rows: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  className: PropTypes.string,
  label: PropTypes.string,
  placeholder: PropTypes.string,
  help: PropTypes.string,
  disabled: PropTypes.bool,
  errors: PropTypes.array,
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired
}

export default Textarea
