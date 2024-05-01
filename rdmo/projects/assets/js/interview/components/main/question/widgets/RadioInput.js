import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty } from 'lodash'

import AdditionalTextInput from './common/AdditionalTextInput'
import AdditionalTextareaInput from './common/AdditionalTextareaInput'
import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'

const RadioInput = ({ value, options, disabled, isDefault, updateValue }) => {
  console.log(value.text)

  const handleChange = (option) => {
    if (option.has_provider) {
      updateValue(value, { text: option.text, external_id: option.id })
    } else {
      updateValue(value, { option: option.id })
    }
  }

  const handleAdditionalValueChange = useDebouncedCallback((value, option, additionalInput) => {
    updateValue(value, {
      option: option.id,
      text: additionalInput
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
                  checked={option.has_provider ? (value.external_id === option.id) : (value.option === option.id)}
                  disabled={disabled}
                  onChange={() => handleChange(option)}
                />
                <OptionText option={option} />
                {
                  isEmpty(option.additional_input) && (
                    <OptionHelp className="ml-10" option={option} />
                  )
                }
                {
                  option.additional_input == 'text' && (
                    <>
                      <span>:</span>
                      <AdditionalTextInput
                        className="ml-10"
                        value={value}
                        option={option}
                        disabled={disabled}
                        onChange={handleAdditionalValueChange}
                      />
                      <OptionHelp className="ml-10" option={option} />
                    </>
                  )
                }
                {
                  option.additional_input == 'textarea' && (
                    <>
                      <span>:</span>
                      <AdditionalTextareaInput
                        value={value}
                        option={option}
                        disabled={disabled}
                        onChange={handleAdditionalValueChange}
                      />
                      <div>
                        <OptionHelp option={option} />
                      </div>
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
