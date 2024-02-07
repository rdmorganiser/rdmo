import React from 'react'
import PropTypes from 'prop-types'
import ReactSelect from 'react-select'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import Link from 'rdmo/core/assets/js/components/Link'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const MultiSelect = ({ config, element, field, options, addText, createText, onChange, onCreate, onEdit }) => {
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

  const values = isNil(element[field]) ? [] : element[field]

  const selectOptions = options.map(option => ({
    value: option.id,
    label: option.uri || option.text || option.name
  }))

  const styles = onEdit ? {
    container: provided => ({...provided, marginRight: 8 + 12 + 4 + 11})
  } : {}

  const handleAdd = () => {
    values.push(selectOptions[0].value)
    onChange(field, values)
  }

  const handleChange = (option, index) => {
    values[index] = option.value
    onChange(field, values)
  }

  const handleRemove = (index) => {
    values.splice(index, 1)
    onChange(field, values)
  }

  const handleEdit = (index) => {
    onEdit(values[index])
  }

  return (
    <div className={className}>
      <label className="control-label" htmlFor={id}>{label}</label>

      <div>
      {
        values.map((value, index) => {
          const selectValue = selectOptions.find(option => (option.value == value))

          return (
            <div key={index} className="multi-select-item mb-10">
              {
                onEdit && <div className="multi-select-item-options">
                  <Link className="fa fa-pencil" title={gettext('Edit')} onClick={() => handleEdit(index)} />
                  <Link className="fa fa-times" title={gettext('Remove')} onClick={() => handleRemove(index)}
                        disabled={element.read_only} />
                </div>
              }

              <ReactSelect classNamePrefix="react-select" className="react-select" styles={styles}
                           options={selectOptions} value={selectValue} isDisabled={element.read_only}
                           onChange={option => handleChange(option, index)} />
            </div>
          )
        })
      }
      </div>

      <button className="btn btn-primary btn-xs" onClick={() => handleAdd()} disabled={element.read_only}>
        {addText}
      </button>

      {
        onCreate &&
        <button className="btn btn-success btn-xs ml-10" onClick={onCreate}
                disabled={element.read_only || isNil(element.id)}
                title={isNil(element.id) ? gettext('For this action, the element must first be created.') : undefined}>
          {createText}
        </button>
      }

      {help && <p className="help-block">{help}</p>}
    </div>
  )
}

MultiSelect.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  options: PropTypes.array,
  addText: PropTypes.string,
  createText: PropTypes.string,
  onChange: PropTypes.func,
  onCreate: PropTypes.func,
  onEdit: PropTypes.func
}

export default MultiSelect
