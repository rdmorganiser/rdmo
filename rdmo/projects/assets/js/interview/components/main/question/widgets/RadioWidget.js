import React from 'react'
import PropTypes from 'prop-types'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty } from 'lodash'

import AdditionalTextInput from './common/AdditionalTextInput'
import AdditionalTextareaInput from './common/AdditionalTextareaInput'
import AddValue from './common/AddValue'
import RemoveValue from './common/RemoveValue'

const RadioInput = ({ value, options, disabled, updateValue }) => {

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

  return (
    <div className="radio-control">
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
  updateValue: PropTypes.func.isRequired
}

const RadioWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
  return (
    <div className="interview-collection">
      {
        values.map((value, valueIndex) => (
          <div key={valueIndex} className="interview-input">
            <div className="interview-input-options">
              {
                question.is_collection && <RemoveValue value={value} deleteValue={deleteValue} />
              }
            </div>
            <RadioInput
              value={value}
              options={question.options}
              disabled={disabled}
              updateValue={updateValue}
            />
          </div>
        ))
      }
      {
        question.is_collection && (
          <AddValue question={question} values={values} currentSet={currentSet} createValue={createValue} />
        )
      }
    </div>
  )
}

RadioWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default RadioWidget
