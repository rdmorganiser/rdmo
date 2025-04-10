import React from 'react'
import ReactSelect from 'react-select'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isArray, isEmpty, isNil, uniqueId } from 'lodash'

const Select = ({ className, label, help, placeholder, isClearable, isDisabled, isMulti, options, errors, value, onChange }) => {
  const id = uniqueId('select-')

  // lookup value(s) in the options array
  const getValue = () => (
    isArray(value) ? options.filter(option => (value.includes(option.value)))
                   : options.find(option => (option.value == value))
  )

  const handleChange = (option) => {
    if (isNil(option)) {
      onChange(null)
    } else if (isArray(option)) {
      onChange(option.map(option => option.value))
    } else {
      onChange(option.value)
    }
  }

  return (
    <div className={classNames('form-group', className)}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <ReactSelect
        classNamePrefix="react-select"
        className={classNames('react-select', {
          'is-invalid': !isEmpty(errors)
        })}
        classNames={{
          control: () => classNames('form-select')
        }}
        placeholder={placeholder}
        isClearable={isClearable}
        isDisabled={isDisabled}
        isMulti={isMulti}
        options={options}
        value={getValue()}
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

Select.propTypes = {
  className: PropTypes.string,
  label: PropTypes.string,
  help: PropTypes.string,
  placeholder: PropTypes.string,
  isClearable: PropTypes.bool,
  isDisabled: PropTypes.bool,
  isMulti: PropTypes.bool,
  options: PropTypes.array,
  errors: PropTypes.array,
  value: PropTypes.oneOfType([PropTypes.array, PropTypes.string]),
  onChange: PropTypes.func.isRequired
}

export default Select
