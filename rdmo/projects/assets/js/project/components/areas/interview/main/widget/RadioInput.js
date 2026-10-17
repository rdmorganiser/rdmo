import React, { useRef } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty } from 'lodash'

import useAdditionalInputs from '../../../../../hooks/useAdditionalInputs'
import useAdjustLabel from '../../../../../hooks/useAdjustLabel'
import { getQuestionHelpId, getQuestionTextId } from '../../../../../utils/question'
import { isDefaultValue } from '../../../../../utils/value'

import AdditionalTextareaInput from './common/AdditionalTextareaInput'
import AdditionalTextInput from './common/AdditionalTextInput'
import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'

const RadioInput = ({ question, value, options, buttons, disabled, onChange }) => {
  const ref = useRef(null)

  const [getAdditionalInput, setAdditionalInput] = useAdditionalInputs(value, options)

  useAdjustLabel(ref)

  const handleChange = (option) => {
    handleAdditionalInputChange.cancel()

    if (option.has_provider) {
      onChange(value, {
        text: option.text,
        external_id: option.id,
        unit: question.unit,
        value_type: question.value_type
      })
    } else {
      onChange(value, {
        text: getAdditionalInput(option) || option.default_text || '',
        option: option.id,
        unit: question.unit,
        value_type: question.value_type
      })
    }
  }

  const handleAdditionalInputChange = useDebouncedCallback((value, option, additionalInput) => {
    onChange(value, {
      option: option.id,
      text: additionalInput,
      unit: question.unit,
      value_type: question.value_type
    })
  }, 500)

  const classnames = classNames('d-flex flex-column gap-2', {
    'text-muted': disabled,
    'default': isDefaultValue(question, value)
  })

  return (
    <div ref={ref} className="project-interview-input radio-input">
      <div className="buttons-wrapper">
        {buttons}
        <fieldset
          className={classnames}
          aria-labelledby={getQuestionTextId(question)}
          aria-describedby={getQuestionHelpId(question)}>
          {
            isEmpty(options) ? (
              <div className="text-muted">{gettext('No options are available.')}</div>
            ) : (
              options.map((option, optionIndex) => {
                const id = `radio-${value.tmp_id || value.id}-${option.id}`

                return (
                  <div key={optionIndex} className="d-flex align-items-top gap-2">
                    <div className="form-check">
                      <input
                        id={id}
                        type="radio"
                        className="form-check-input"
                        checked={option.has_provider ? (value.external_id === option.id) : (value.option === option.id)}
                        disabled={disabled}
                        aria-label={option.text}
                        onChange={() => handleChange(option)}
                      />
                      <label className="form-check-label" htmlFor={id}>
                        <OptionText option={option} />
                      </label>
                    </div>
                    {
                      isEmpty(option.additional_input) && (
                        <OptionHelp className="ml-10" option={option} />
                      )
                    }
                    {
                      option.additional_input == 'text' && (
                        <>
                          <AdditionalTextInput
                            className=""
                            inputValue={getAdditionalInput(option)}
                            disabled={disabled}
                            onChange={
                              (additionalInput) => {
                                setAdditionalInput(option, additionalInput)
                                handleAdditionalInputChange(value, option, additionalInput)
                              }
                            }
                          />
                          <OptionHelp className="ml-10" option={option} />
                        </>
                      )
                    }
                    {
                      option.additional_input == 'textarea' && (
                        <>
                          <AdditionalTextareaInput
                            inputValue={getAdditionalInput(option)}
                            disabled={disabled}
                            onChange={
                              (additionalInput) => {
                                setAdditionalInput(option, additionalInput)
                                handleAdditionalInputChange(value, option, additionalInput)
                              }
                            }
                          />
                          <OptionHelp option={option} />
                        </>
                      )
                    }
                  </div>
                )
              })
            )
          }
        </fieldset>
      </div>
    </div>
  )
}

RadioInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  buttons: PropTypes.node.isRequired,
  disabled: PropTypes.bool.isRequired,
  onChange: PropTypes.func.isRequired,
}

export default RadioInput
