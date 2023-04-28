import React, { Component} from 'react'
import ReactSelect from 'react-select'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const Select = ({ config, element, field, options, verboseName, isMulti, onChange, onCreate, onEdit }) => {
  const id = getId(element, field),
        label = getLabel(config, element, field),
        help = getHelp(config, element, field),
        warnings = get(element, ['warnings', field]),
        errors = get(element, ['errors', field])

  const className = classNames({
    'form-group': true,
    'has-warning': !isEmpty(warnings),
    'has-error': !isEmpty(errors)
  })

  const selectOptions = options.map(option => ({
    value: option.id,
    label: option.uri || option.text || option.name
  }))

  const selectValue = selectOptions.find(option => (option.value == element[field]))

  const styles = onEdit ? {
    container: provided => ({...provided, marginRight: 50})
  } : {}

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <div className="select-item">
        {
          onEdit && <div className="pull-right">
            <button className="btn btn-primary ml-5" onClick={() => onEdit(selectValue.value)} disabled={isNil(selectValue)}>
              {gettext('Edit')}
            </button>
          </div>
        }

        <ReactSelect classNamePrefix="react-select" className="react-select" isClearable={true}
                     options={selectOptions} value={selectValue} isMulti={isMulti}
                     onChange={option => onChange(field, isNil(option) ? null : option.value)}
                     styles={styles} />
      </div>

      {
        onCreate && <button className="btn btn-success btn-xs mt-10" onClick={onCreate}>
          {interpolate(gettext('Create new %s'), [verboseName])}
        </button>
      }

      {help && <p className="help-block">{help}</p>}

      {errors && <ul className="help-block list-unstyled">
        {errors.map((error, index) => <li key={index}>{error}</li>)}
      </ul>}
    </div>
  )
}

Select.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  options: PropTypes.array,
  isMulti: PropTypes.bool,
  onChange: PropTypes.func,
  onCreate: PropTypes.func,
  onEdit: PropTypes.func
}

export default Select
