import React from 'react'
import PropTypes from 'prop-types'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty, isNil } from 'lodash'

import AdditionalTextInput from './common/AdditionalTextInput'
import AdditionalTextareaInput from './common/AdditionalTextareaInput'

const CheckboxInput = ({ value, option, disabled, onCreate, onUpdate, onDelete }) => {

  const checked = !isNil(value)

  const handleChange = () => {
    if (checked) {
      onDelete(value)
    } else {
      onCreate(option)
    }
  }

  const handleAdditionalValueChange = useDebouncedCallback((value, option, additionalValue) => {
    if (checked) {
      onUpdate(value, { text: additionalValue, option: option.id })
    } else {
      onCreate(option, additionalValue)
    }
  }, 500)

  return (
    <div className="checkbox">
      <label>
        <input
          type="checkbox"
          checked={checked}
          disabled={disabled}
          onChange={() => handleChange()}
        />
        <span>{option.text}</span>
        {
          isEmpty(option.additional_input) && (
            <span className="text-muted">{option.help}</span>
          )
        }
        {
          option.additional_input == 'text' && (
            <>
              <span>:</span>
              {' '}
              <AdditionalTextInput value={value} option={option} disabled={disabled} onChange={handleAdditionalValueChange} />
              {' '}
              <span className="text-muted">{option.help}</span>
            </>
          )
        }
        {
          option.additional_input == 'textarea' && (
            <>
              <span>:</span>
              {' '}
              <AdditionalTextareaInput value={value} option={option} disabled={disabled} onChange={handleAdditionalValueChange} />
              {' '}
              <div className="text-muted">{option.help}</div>
            </>
          )
        }
      </label>
    </div>
  )
}

CheckboxInput.propTypes = {
  value: PropTypes.object,
  option: PropTypes.object,
  disabled: PropTypes.bool,
  onCreate: PropTypes.func.isRequired,
  onUpdate: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default CheckboxInput
