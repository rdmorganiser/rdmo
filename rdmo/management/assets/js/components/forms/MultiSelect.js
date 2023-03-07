import React, { Component } from 'react'
import PropTypes from 'prop-types'
import ReactSelect from 'react-select'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const MultiSelect = ({ config, element, field, warnings, errors, options, verboseName, onChange }) => {
  const id = getId(element, field),
        label = getLabel(config, element, field),
        help = getHelp(config, element, field),
        warningList = warnings[field],
        errorList = errors[field]

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warningList),
    'has-error': !isEmpty(errorList)
  })

  const values = element[field]

  const selectOptions = options.map(option => ({
    value: option.id,
    label: option.uri || option.text || option.name
  }))

  const handleAdd = () => {
    values.push(null)
    onChange(field, values)
  }

  const handleChange = (option, index) => {
    if (isNil(option)) {
      // remove this value
      values.splice(index, 1)
    } else {
      values[index] = option.value
    }
    onChange(field, values)
  }

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <div>
      {
        values.map((value, index) => {
          const selectValue = selectOptions.find(option => (option.value == value))

          return (
            <div key={index} className="mb-10">
              <ReactSelect classNamePrefix="react-select" className="react-select" isClearable={true}
                           options={selectOptions} value={selectValue}
                           onChange={option => handleChange(option, index)} />
            </div>
          )
        })
      }
      </div>

      <button className="btn btn-default btn-sm" onClick={() => handleAdd()}>
        {interpolate(gettext('Add %s'), [verboseName])}
      </button>

      {help && <p className="help-block">{help}</p>}
    </div>
  )
}

MultiSelect.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  options: PropTypes.array,
  verboseName: PropTypes.string,
  onChange: PropTypes.func
}

export default MultiSelect
