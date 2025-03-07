import React, { Component, useRef } from 'react'
import ReactSelect from 'react-select'
import { useDrag, useDrop } from 'react-dnd'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isUndefined from 'lodash/isUndefined'
import isNil from 'lodash/isNil'
import isNumber from 'lodash/isNumber'
import toNumber from 'lodash/toNumber'
import get from 'lodash/get'
import maxBy from 'lodash/maxBy'

import Link from 'rdmo/core/assets/js/components/Link'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const OrderedMultiSelectItem = ({ index, field, selectValue, selectOptions, errors, disabled, ariaLabelledBy,
                                  handleChange, handleEdit, handleRemove, handleDrag }) => {
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

  const dropClassName = classNames({
    'drop': true,
    'show': isDragging,
    'over': isOver
  })

  const dragClassName = classNames({
    'fa fa-arrows drag': true,
    disabled: disabled
  })

  if (!disabled) {
    drag(dragRef)
    drop(dropRef)
  }

  const styles = {
    container: provided => ({...provided, marginRight: 8 + 12 + 4 + 11 + 4 + 14})
  }

  return (
    <>
      <div className="ordered-multi-select-item">
        <div className="ordered-multi-select-item-options">
          <Link className="fa fa-pencil" title={gettext('Edit')}
                onClick={() => handleEdit(index)} />
          <Link className="fa fa-times" title={gettext('Remove')} disabled={disabled}
                onClick={() => !disabled && handleRemove(index)} />
          <i className={dragClassName} ref={dragRef} aria-hidden="true"></i>
        </div>
        <div className="ordered-multi-select-item-select">
          <ReactSelect classNamePrefix="react-select" className="react-select"
                       options={selectOptions} value={selectValue}
                       onChange={option => handleChange(option, index)}
                       menuPortalTarget={document.body} styles={styles} isDisabled={disabled}
                       aria-labelledby={ariaLabelledBy} />
        </div>
        {
          errors && errors[index] &&
          <ul className="help-block list-unstyled">
            {
              Object.keys(errors[index]).map((key, i1) => {
                return errors[index][key].map((error, i2) => <li key={`${i1}-${i2}`}>{error}</li>)
              })
            }
          </ul>
        }
      </div>
      <div ref={dropRef} className={dropClassName}></div>
    </>
  )
}

class OrderedMultiSelect extends Component {

  constructor(props) {
    super(props)

    this.handleChange = this.handleChange.bind(this)
    this.handleEdit = this.handleEdit.bind(this)
    this.handleRemove = this.handleRemove.bind(this)
    this.handleDrag = this.handleDrag.bind(this)
  }

  getValues() {
    const { field, values, element } = this.props

    if (isUndefined(values)) {
      return isUndefined(element[field]) ? [] : [...element[field]]
    } else {
      return values
    }
  }

  getSelectOptions() {
    const { options } = this.props

    return options.map(option => ({
      value: option.value || option.id,
      label: option.label || option.uri || option.text || option.name
    }))
  }

  parseValue(option) {
    const { field } = this.props

    if (isNumber(option.value)) {
      return [field.slice(0, -1), option.value]
    } else {
      const [valueField, id] = option.value.split('-')
      return [valueField, toNumber(id)]
    }
  }

  compareValue(option, value) {
    const valueField = Object.keys(value).filter(k => k != 'order')[0]
    if (isNumber(option.value)) {
      return option.value == value[valueField]
    } else {
      return option.value == valueField + '-' + value[valueField]
    }
  }

  handleAdd() {
    const { field, onChange } = this.props
    const values = this.getValues()

    const maxValue = maxBy(values, 'order')
    const [valueField, value] = this.parseValue(this.getSelectOptions()[0])
    values.push({
      [valueField]: value,
      order: maxValue ? maxValue.order + 1 : 0
    })

    onChange(field, values)
  }

  handleChange(option, index) {
    const { field, onChange } = this.props
    const values = this.getValues()

    if (isNil(option)) {
      values[index] = null
    } else {
      const [valueField, value] = this.parseValue(option)
      values[index] = {
        [valueField]: value,
        order: values[index].order
      }
    }

    onChange(field, values)
  }

  handleEdit(index) {
    const { onEdit } = this.props
    const values = this.getValues()

    onEdit(values[index])
  }

  handleRemove(index) {
    const { field, onChange } = this.props
    const values = this.getValues()

    values.splice(index, 1)

    onChange(field, values)
  }

  handleDrag(dragIndex, dropIndex) {
    const { field, onChange } = this.props
    const values = this.getValues()

    const dragValue = values[dragIndex]
    values.splice(dragIndex, 1)
    values.splice(dropIndex, 0, dragValue)

    // re-order the array
    values.forEach((value, index) => {
      value.order = index
    })

    onChange(field, values)
  }

  render() {
    const { config, element, field, addText, createText, altCreateText,
            onCreate, onAltCreate } = this.props

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

    return (
      <div className={className}>
        <div className="mb-5">
          <strong id={id}>{label}</strong>
        </div>

        <div>
        {
          this.getValues().map((value, index) => {
            const selectOptions = this.getSelectOptions()
            const selectValue = selectOptions.find(option => this.compareValue(option, value))
            return (
              <OrderedMultiSelectItem key={index} index={index} field={field}
                                      selectValue={selectValue} selectOptions={selectOptions}
                                      errors={errors} handleChange={this.handleChange}
                                      handleEdit={this.handleEdit} handleRemove={this.handleRemove}
                                      handleDrag={this.handleDrag} ariaLabelledBy={id} disabled={element.read_only} />
            )
          })
        }
        </div>

        <button type="button" className="btn btn-primary btn-xs" onClick={() => this.handleAdd()}
                disabled={element.read_only}>
          {addText}
        </button>
        {
          onCreate &&
          <button type="button" className="btn btn-success btn-xs ml-10" onClick={onCreate}
                  disabled={element.read_only || isNil(element.id)}
                  title={isNil(element.id) ? gettext('For this action, the element must first be created.') : undefined}>
            {createText}
          </button>
        }
        {
          onAltCreate &&
          <button type="button" className="btn btn-success btn-xs ml-10" onClick={onAltCreate}
                  disabled={element.read_only || isNil(element.id)}
                  title={isNil(element.id) ? gettext('For this action, the element must first be created.') : undefined}>
            {altCreateText}
          </button>
        }

        {help && <p className="help-block">{help}</p>}
      </div>
    )
  }
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
  config: PropTypes.object.isRequired,
  element: PropTypes.object.isRequired,
  field: PropTypes.string.isRequired,
  fields: PropTypes.array,
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
