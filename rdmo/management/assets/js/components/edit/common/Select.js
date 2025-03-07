import React from 'react'
import ReactSelect from 'react-select'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import get from 'lodash/get'
import isArray from 'lodash/isArray'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import Link from 'rdmo/core/assets/js/components/Link'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const Select = ({ config, element, field, options, createText, isMulti, onChange, onCreate, onEdit }) => {
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

  const selectValue = isArray(element[field]) ? selectOptions.filter(option => (element[field].includes(option.value)))
                                              : selectOptions.find(option => (option.value == element[field]))

  const styles = onEdit && selectValue ? {
    container: provided => ({...provided, marginRight: 8 + 12})
  } : {}

  const handleChange = (option) => {
    if (isNil(option)) {
      onChange(field, null)
    } else if (isArray(option)) {
      onChange(field, option.map(o => o.value))
    } else {
      onChange(field, option.value)
    }
  }

  return (
    <div className={className}>
      <div className="mb-5">
        <strong id={id}>{label}</strong>
      </div>

      <div className="select-item">
        {
          onEdit && selectValue && <div className="select-item-options">
            <Link className="fa fa-pencil" title={gettext('Edit')}
                  onClick={() => onEdit(selectValue.value)} disabled={isNil(selectValue)} />
          </div>
        }

        <ReactSelect classNamePrefix="react-select" className="react-select" isClearable={true}
                     options={selectOptions} value={selectValue} isMulti={isMulti}
                     onChange={handleChange} styles={styles} isDisabled={element.read_only} aria-labelledby={id} />
      </div>


      {
        onCreate &&
        <button type="button" className="btn btn-success btn-xs mt-10" onClick={onCreate} disabled={isNil(element.id)}
                title={isNil(element.id) ? gettext('For this action, the element must first be created.') : undefined}>
          {createText}
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
  createText: PropTypes.string,
  isMulti: PropTypes.bool,
  onChange: PropTypes.func,
  onCreate: PropTypes.func,
  onEdit: PropTypes.func
}

export default Select
