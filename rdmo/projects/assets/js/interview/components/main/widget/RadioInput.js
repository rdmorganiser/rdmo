import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty } from 'lodash'

import { isDefaultValue } from '../../../utils/value'

import AdditionalTextInput from './common/AdditionalTextInput'
import AdditionalTextareaInput from './common/AdditionalTextareaInput'
import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'

const RadioInput = ({ question, value, options, disabled, updateValue, buttons }) => {
  const handleChange = (option) => {
    if (option.has_provider) {
      updateValue(value, {
        text: option.text,
        external_id: option.id,
        unit: question.unit,
        value_type: question.value_type
      })
    } else {
      updateValue(value, {
        option: option.id,
        unit: question.unit,
        value_type: question.value_type
      })
    }
  }

  const handleAdditionalValueChange = useDebouncedCallback((value, option, additionalInput) => {
    updateValue(value, {
      option: option.id,
      text: additionalInput,
      unit: question.unit,
      value_type: question.value_type
    })
  }, 500)

  const classnames = classNames('radio-control', {
    'text-muted': disabled,
    'default': isDefaultValue(question, value)
  })

  return (
    <div className="interview-input radio-input">
      <div className="buttons-wrapper">
        {buttons}
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
      </div>
    </div>
  )
}

RadioInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default RadioInput
