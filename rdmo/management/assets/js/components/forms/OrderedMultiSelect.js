import React, { Component} from 'react'
import ReactSelect from 'react-select'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const OrderedMultiSelect = ({ config, element, field, selectField, warnings, errors, options, onChange }) => {
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
    // add an empty value to the value array and call onChange
    values.push({
      [selectField]: null,
      order: values.reduce((acc, cur) => (cur.order > acc) ? cur.order : acc, 0)
    })
    onChange(field, values)
  }

  const handleChange = (option, index) => {
    if (isNil(option)) {
      // remove this value
      values.splice(index, 1)
    } else {
      values[index][selectField] = option.value
    }
    onChange(field, values)
  }

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <div>
      {
        values.map((value, index) => {
          const selectValue = selectOptions.find(option => (option.value == value[selectField]))

          return (
            <div key={index} className="mb-10">
              <div>
                <ReactSelect classNamePrefix="react-select" isClearable={true}
                             options={selectOptions} value={selectValue}
                             onChange={option => handleChange(option, index)} />
              </div>
              {
                errorList && errorList[index] &&
                <ul className="help-block list-unstyled">
                  {
                    errorList[index][selectField] &&
                    errorList[index][selectField].map((error, i) => <li key={i}>{error}</li>)
                  }
                  {
                    errorList[index].order &&
                    errorList[index].order.map((error, i) => <li key={i}>order: {error}</li>)
                  }
                </ul>
              }
            </div>
          )
        })
      }
      </div>

      <button className="btn btn-default btn-sm" onClick={() => handleAdd()}>
        {interpolate(gettext('Add %s'), [selectField])}
      </button>

      {help && <p className="help-block">{help}</p>}
    </div>
  )
}

OrderedMultiSelect.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  selectField: PropTypes.string,
  warnings: PropTypes.object,
  errors: PropTypes.object,
  options: PropTypes.array,
  onChange: PropTypes.func
}

export default OrderedMultiSelect
