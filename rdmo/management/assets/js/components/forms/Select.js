import React, { Component} from 'react'
import ReactSelect from 'react-select'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import { getLabel, getHelp } from 'rdmo/management/assets/js/utils/meta'

const Select = ({ config, element, elementType, field, warnings, errors, options, onChange }) => {
  const id = `${elementType}-${field}`,
        label = getLabel(config, elementType, field),
        help = getHelp(config, elementType, field),
        warningList = warnings[field],
        errorList = errors[field]

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warningList),
    'has-error': !isEmpty(errorList)
  })

  const selectOptions = options.map(option => ({
    value: option.id,
    label: option.uri || option.text
  }))

  const selectValue = selectOptions.find(option => (option.value == element[field]))

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <ReactSelect classNamePrefix="react-select" isClearable={true}
                   options={selectOptions} value={selectValue}
                   onChange={option => onChange(field, isNil(option) ? null : option.value)} />

      {help && <p className="help-block">{help}</p>}

      {errorList && <ul className="help-block list-unstyled">
        {errorList.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

Select.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  options: PropTypes.array,
  onChange: PropTypes.func
}

export default Select
