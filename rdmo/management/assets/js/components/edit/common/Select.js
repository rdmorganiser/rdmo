import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'
import ReactSelect from 'react-select'
import classNames from 'classnames'
import get from 'lodash/get'
import isArray from 'lodash/isArray'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'

import { getHelp, getId, getLabel } from 'rdmo/management/assets/js/utils/forms'

import Link from 'rdmo/core/assets/js/components/Link'

import ErrorList from './ErrorList'
import HelpText from './HelpText'

const Select = ({ element, field, options, createText, isMulti, onChange, onCreate, onEdit }) => {
  const { meta } = useSelector((state) => state.config)

  const id = getId(element, field),
    label = getLabel(element, field, meta),
    help = getHelp(element, field, meta),
    errors = get(element, ['errors', field])

  const className = classNames('d-flex align-items-center gap-2', {
    'is-invalid': !isEmpty(errors)
  })

  const selectClassNames = {
    control: () => classNames('form-control', {
      'is-invalid': !isEmpty(errors)
    })
  }

  const selectOptions = options.map(option => ({
    value: option.id,
    label: option.uri || option.text || option.name
  }))

  const selectValue = isArray(element[field]) ? selectOptions.filter(option => (element[field].includes(option.value))): selectOptions.find(option => (option.value == element[field]))

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
    <div className="mb-3">
      <div className="mb-2">
        <strong id={id}>{label}</strong>
      </div>

      <div className={className}>
        <div className="flex-grow-1">
          <ReactSelect classNamePrefix="react-select" className="react-select" classNames={selectClassNames}
            options={selectOptions} value={selectValue} isMulti={isMulti} isClearable={true}
            onChange={handleChange} isDisabled={element.read_only} aria-labelledby={id} />
        </div>
        {
          onEdit && selectValue && <div>
            <Link className="bi bi-pencil" title={gettext('Edit')}
              onClick={() => onEdit(selectValue.value)} disabled={isNil(selectValue)} />
          </div>
        }
      </div>

      {
        onCreate &&
        <div className="mt-2">
          <button type="button" className="btn btn-success btn-sm" onClick={onCreate} disabled={isNil(element.id)}
            title={isNil(element.id) ? gettext('For this action, the element must first be created.') : undefined}>
            {createText}
          </button>
        </div>
      }

      <ErrorList errors={errors} />
      <HelpText help={help} />
    </div>
  )
}

Select.propTypes = {
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
