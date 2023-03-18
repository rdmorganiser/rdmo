import React, { Component, useRef } from 'react'
import ReactSelect from 'react-select'
import { useDrag, useDrop } from 'react-dnd'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import isEmpty from 'lodash/isEmpty'
import isNil from 'lodash/isNil'
import get from 'lodash/get'

import { getId, getLabel, getHelp } from 'rdmo/management/assets/js/utils/forms'

const OrderedMultiSelectItem = ({ index, field, selectValue, selectOptions,
                                  errors, handleChange, handleDrag }) => {
  const ref = useRef(null)

  const [{ isOver }, drop] = useDrop(() => ({
    accept: field,
    // drop: (item, monitor) => handleDrag(item.index, index),
    collect: (monitor) => ({
      isOver: monitor.isOver()
    }),
    hover: (item, monitor) => {
      if (!ref.current || item.index === index) {
        return
      } else {
        handleDrag(item.index, index)
        item.index = index
      }
    }
  }))

  const [{}, drag] = useDrag(() => ({
    type: field,
    item: { index }
  }))

  const className = classNames({
    'ordered-multi-select-item': true,
    'mb-10': true,
    'over': isOver
  })

  drag(drop(ref))

  return (
    <div ref={ref} className={className}>
      <div>
        <div className="handle pull-left text-left">
          <i className="fa fa-ellipsis-v"></i>
        </div>
        <div className="handle pull-right text-right">
          <i className="fa fa-ellipsis-v"></i>
        </div>
        <div>
          <ReactSelect classNamePrefix="react-select" className="react-select" isClearable={true}
                       options={selectOptions} value={selectValue}
                       onChange={option => handleChange(option, index)}
                       menuPortalTarget={document.body} />
        </div>
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
  )
}

const OrderedMultiSelect = ({ config, element, field, options, verboseName, onChange }) => {
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

  const handleAdd = () => {
    // add an empty value to the value array and call onChange
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

  const handleDrag = (dragIndex, dropIndex) => {
    const value = values[dragIndex]
    values.splice(dragIndex, 1)
    values.splice(dropIndex, 0, value)
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
            <OrderedMultiSelectItem key={index} index={index} field={field}
                                    selectValue={selectValue} selectOptions={selectOptions}
                                    errors={errors} handleChange={handleChange} handleDrag={handleDrag} />
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

OrderedMultiSelectItem.propTypes = {
  index: PropTypes.number,
  field: PropTypes.string,
  selectValue: PropTypes.object,
  selectOptions: PropTypes.array,
  errors: PropTypes.object,
  onChange: PropTypes.func,
  onDrag: PropTypes.func
}

OrderedMultiSelect.propTypes = {
  config: PropTypes.object,
  element: PropTypes.object,
  field: PropTypes.string,
  options: PropTypes.array,
  verboseName: PropTypes.string,
  onChange: PropTypes.func
}

export default OrderedMultiSelect
