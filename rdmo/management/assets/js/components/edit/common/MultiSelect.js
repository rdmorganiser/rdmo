import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import ReactSelect from 'react-select'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import Link from 'rdmo/core/assets/js/components/Link'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

import ErrorList from './ErrorList'
import HelpText from './HelpText'

const MultiSelect = ({ element, field, options, addText, createText, onChange, onCreate, onEdit }) => {
  const { meta } = useSelector((state) => state.config)

  const id = getId(element, field),
        label = getLabel(element, field, meta),
        help = getHelp(element, field, meta),
        errors = get(element, ['errors', field])

  const className = classNames({
    'is-invalid': !isEmpty(errors)
  })

  const selectClassNames = {
    control: () => classNames('form-control', {
      'is-invalid': !isEmpty(errors)
    })
  }

  const values = isNil(element[field]) ? [] : element[field]

  const selectOptions = options.map(option => ({
    value: option.id,
    label: option.uri || option.text || option.name
  }))

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
    <div className="mb-3">
      <div className="mb-2">
        <strong id={id}>{label}</strong>
      </div>

      <div className={className}>
      {
        values.map((value, index) => {
          const selectValue = selectOptions.find(option => (option.value == value))

          return (
            <div key={index} className="d-flex align-items-center gap-2 mb-2">
              <div className="flex-grow-1">
                <ReactSelect classNamePrefix="react-select" className="react-select" classNames={selectClassNames}
                             options={selectOptions} value={selectValue} isDisabled={element.read_only}
                             aria-labelledby={id} onChange={option => handleChange(option, index)} />
              </div>
              {
                onEdit && <div className="d-flex align-items-center gap-1">
                  <Link className="bi bi-pencil" title={gettext('Edit')} onClick={() => handleEdit(index)} />
                  <Link className="bi bi-x-lg" title={gettext('Remove')} onClick={() => handleRemove(index)}
                        disabled={element.read_only} />
                </div>
              }
            </div>
          )
        })
      }
      </div>

      <div className="d-flex align-items-center gap-2">
        <button type="button" className="btn btn-primary btn-sm" onClick={() => handleAdd()}
                disabled={element.read_only}>
          {addText}
        </button>

        {
          onCreate &&
          <button type="button" className="btn btn-success btn-sm" onClick={onCreate}
                  disabled={element.read_only || isNil(element.id)}
                  title={isNil(element.id) ? gettext('For this action, the element must first be created.') : undefined}>
            {createText}
          </button>
        }
      </div>

      <ErrorList errors={errors} />
      <HelpText help={help} />
    </div>
  )
}

MultiSelect.propTypes = {
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
