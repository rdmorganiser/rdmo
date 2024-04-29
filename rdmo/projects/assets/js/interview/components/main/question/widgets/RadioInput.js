import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty } from 'lodash'

import AdditionalTextInput from './common/AdditionalTextInput'
import AdditionalTextareaInput from './common/AdditionalTextareaInput'

const RadioInput = ({ value, options, disabled, isDefault, updateValue }) => {

  const handleChange = (option) => {
    if (isEmpty(option.additional_input)) {
      updateValue(value, { option: option.id, text: '' })
    } else {
      updateValue(value, { option: option.id })
    }
  }

  const handleAdditionalValueChange = useDebouncedCallback((value, option, additionalValue) => {
    updateValue(value, {
      option: option.id,
      text: additionalValue
    })
  }, 500)

  const classnames = classNames({
    'radio-control': true,
    'default': isDefault
  })

  return (
    <div className={classnames}>
      {
        isEmpty(options) ? (
          <div className="text-muted">{gettext('No options are available.')}</div>
        ) : (
          options.map((option, optionIndex) => (
            <div key={optionIndex} className="radio">
              <label>
                <input
                  type="radio"
                  checked={value.option == option.id}
                  disabled={disabled}
                  onChange={() => handleChange(option)}
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
          ))
        )
      }
    </div>
  )
}

RadioInput.propTypes = {
  value: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  isDefault: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

export default RadioInput
