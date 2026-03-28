import React, { useRef } from 'react'
import PropTypes from 'prop-types'
import { useDrag, useDrop } from 'react-dnd'
import { useSelector } from 'react-redux'
import ReactSelect from 'react-select'
import classNames from 'classnames'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import isNumber from 'lodash/isNumber'
import isUndefined from 'lodash/isUndefined'
import maxBy from 'lodash/maxBy'
import toNumber from 'lodash/toNumber'

import { getHelp, getId, getLabel } from 'rdmo/management/assets/js/utils/forms'

import Link from 'rdmo/core/assets/js/components/Link'

import ErrorList from './ErrorList'
import HelpText from './HelpText'

const OrderedMultiSelectItem = ({
  index, field, selectValue, selectOptions, errors, disabled, ariaLabelledBy,
  handleChange, handleEdit, handleRemove, handleDrag
}) => {
  const dragRef = useRef(null)
  const dropRef = useRef(null)

  const [{}, drag] = useDrag(() => ({
    type: field,
    item: { index }
  }))

  const [{ isDragging, isOver }, drop] = useDrop(() => ({
    accept: field,
    collect: (monitor) => ({
      isDragging: monitor.getItemType() == field,
      isOver: monitor.isOver()
    }),
    drop: (item) => {
      handleDrag(item.index, index)
    },
  }))

  const dropClassName = classNames('drop', {
    'show': isDragging,
    'over': isOver
  })

  const dragClassName = classNames('bi bi-arrows-move drag', {
    disabled: disabled
  })

  if (!disabled) {
    drag(dragRef)
    drop(dropRef)
  }

  const itemErrors = isEmpty(errors) || isEmpty(errors[index]) ? [] : (
    Object.values(errors[index]).reduce((itemErrors, values) => [...itemErrors, ...values]
    ))

  const className = classNames('d-flex align-items-center gap-2', {
    'is-invalid': !isEmpty(itemErrors)
  })

  const selectClassNames = {
    control: () => classNames('form-control', {
      'is-invalid': !isEmpty(itemErrors)
    })
  }

  return (
    <div className="position-relative mb-2">
      <div className={className}>
        <div className="flex-grow-1">
          <ReactSelect
            classNamePrefix="react-select" className="react-select" classNames={selectClassNames}
            options={selectOptions} value={selectValue}
            onChange={option => handleChange(option, index)}
            menuPortalTarget={document.body} isDisabled={disabled}
            aria-labelledby={ariaLabelledBy} />
        </div>
        <Link
          className="bi bi-pencil" title={gettext('Edit')}
          onClick={() => handleEdit(index)} />
        <Link
          className="bi bi-x-lg" title={gettext('Remove')} disabled={disabled}
          onClick={() => !disabled && handleRemove(index)} />
        <i className={dragClassName} ref={dragRef} aria-hidden="true"></i>
      </div>

      <ErrorList errors={itemErrors} />

      <div ref={dropRef} className={dropClassName}></div>
    </div>
  )
}


const OrderedMultiSelect = ({
  element, field, options, values,
  addText, createText, altCreateText, onChange, onCreate, onAltCreate, onEdit
}) => {

  const { meta } = useSelector((state) => state.config)

  const id = getId(element, field)
  const label = getLabel(element, field, meta)
  const help = getHelp(element, field, meta)
  const errors = get(element, ['errors', field])

  const getValues = () => {
    if (isUndefined(values)) {
      return isUndefined(element[field]) ? [] : [...element[field]]
    } else {
      return values
    }
  }

  const getSelectOptions = () => {
    return options.map(option => ({
      value: option.value || option.id,
      label: option.label || option.uri || option.text || option.name
    }))
  }

  const parseValue = (option) => {
    if (isNumber(option.value)) {
      return [field.slice(0, -1), option.value]
    } else {
      const [valueField, id] = option.value.split('-')
      return [valueField, toNumber(id)]
    }
  }

  const compareValue = (option, value) => {
    const valueField = Object.keys(value).filter(k => k != 'order')[0]
    if (isNumber(option.value)) {
      return option.value == value[valueField]
    } else {
      return option.value == valueField + '-' + value[valueField]
    }
  }

  const handleAdd = () => {
    const values = getValues()

    const maxValue = maxBy(values, 'order')
    const [valueField, value] = parseValue(getSelectOptions()[0])
    values.push({
      [valueField]: value,
      order: maxValue ? maxValue.order + 1 : 0
    })

    onChange(field, values)
  }

  const handleChange = (option, index) => {
    const values = getValues()

    if (isNil(option)) {
      values[index] = null
    } else {
      const [valueField, value] = parseValue(option)
      values[index] = {
        [valueField]: value,
        order: values[index].order
      }
    }

    onChange(field, values)
  }

  const handleEdit = (index) => {
    const values = getValues()

    onEdit(values[index])
  }

  const handleRemove = (index) => {
    const values = getValues()

    values.splice(index, 1)

    onChange(field, values)
  }

  const handleDrag = (dragIndex, dropIndex) => {
    const values = getValues()

    const dragValue = values[dragIndex]
    values.splice(dragIndex, 1)
    values.splice(dropIndex, 0, dragValue)

    // re-order the array
    values.forEach((value, index) => {
      value.order = index
    })

    onChange(field, values)
  }

  return (
    <div className="mb-3">
      <div className="mb-2">
        <strong id={id}>{label}</strong>
      </div>

      <div>
        {
          getValues().map((value, index) => {
            const selectOptions = getSelectOptions()
            const selectValue = selectOptions.find(option => compareValue(option, value))
            return (
              <OrderedMultiSelectItem
                key={index} index={index} field={field}
                selectValue={selectValue} selectOptions={selectOptions}
                errors={errors} handleChange={handleChange}
                handleEdit={handleEdit} handleRemove={handleRemove}
                handleDrag={handleDrag} ariaLabelledBy={id} disabled={element.read_only} />
            )
          })
        }
      </div>

      <div className="d-flex align-items-center gap-2">
        <button
          type="button" className="btn btn-primary btn-sm" onClick={handleAdd}
          disabled={element.read_only}>
          {addText}
        </button>
        {
          onCreate && (
            <button
              type="button" className="btn btn-success btn-sm" onClick={onCreate}
              disabled={element.read_only || isNil(element.id)}
              title={isNil(element.id) ? gettext('For this action, the element must first be created.') : undefined}>
              {createText}
            </button>
          )
        }
        {
          onAltCreate && (
            <button
              type="button" className="btn btn-success btn-sm" onClick={onAltCreate}
              disabled={element.read_only || isNil(element.id)}
              title={isNil(element.id) ? gettext('For this action, the element must first be created.') : undefined}>
              {altCreateText}
            </button>
          )
        }
      </div>

      <HelpText help={help} />
    </div>
  )
}

OrderedMultiSelectItem.propTypes = {
  index: PropTypes.number,
  field: PropTypes.string,
  selectValue: PropTypes.object,
  selectOptions: PropTypes.array,
  errors: PropTypes.object,
  ariaLabelledBy: PropTypes.string,
  disabled: PropTypes.bool,
  handleChange: PropTypes.func,
  handleEdit: PropTypes.func,
  handleRemove: PropTypes.func,
  handleDrag: PropTypes.func
}

OrderedMultiSelect.propTypes = {
  element: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
  options: PropTypes.array.isRequired,
  values: PropTypes.array,
  addText: PropTypes.string.isRequired,
  createText: PropTypes.string,
  altCreateText: PropTypes.string,
  onChange: PropTypes.func.isRequired,
  onCreate: PropTypes.func,
  onAltCreate: PropTypes.func,
  onEdit: PropTypes.func.isRequired
}

export default OrderedMultiSelect
