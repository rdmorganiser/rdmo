import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty, isNil } from 'lodash'

import QuestionAddValue from '../QuestionAddValue'
import QuestionRemoveValue from '../QuestionRemoveValue'

const RangeInput = ({ value, minimum, maximum, step, disabled, updateValue }) => {
  const [inputValue, setInputValue] = useState('')
  useEffect(() => {setInputValue(value.text)}, [value.id])

  const handleChange = useDebouncedCallback((value, text) => {
    updateValue(value, { text })
  }, 500)

  return (
    <div className="range">
      <span className="badge">{inputValue}</span>
      <input
        type="range"
        min={isEmpty(minimum) ? '0' : minimum}
        max={isEmpty(maximum) ? '100' : maximum}
        step={isEmpty(step) ? '1' : step}
        disabled={disabled}
        value={inputValue}
        onChange={(event) => {
          setInputValue(event.target.value)
          handleChange(value, event.target.value)
        }}
      />
    </div>
  )
}

RangeInput.propTypes = {
  value: PropTypes.object.isRequired,
  minimum: PropTypes.number,
  maximum: PropTypes.number,
  step: PropTypes.number,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

const RangeWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {

  const handleCreateValue = (value) => {
    value.text = isNil(question.minimum) ? 0 : question.minimum
    createValue(value)
  }

  return (
    <div className="interview-collection">
      {
        values.map((value, valueIndex) => (
          <div key={valueIndex} className="interview-input">
            <div className="interview-input-options">
              {
                (question.is_collection || values.length > 1) && (
                  <QuestionRemoveValue value={value} deleteValue={deleteValue} />
                )
              }
            </div>
            <RangeInput
              value={value}
              minimum={question.minimum}
              maximum={question.maximum}
              step={question.step}
              disabled={disabled}
              updateValue={updateValue}
            />
          </div>
        ))
      }
      {
        question.is_collection && (
          <QuestionAddValue question={question} values={values} currentSet={currentSet} createValue={handleCreateValue} />
        )
      }
    </div>
  )
}

RangeWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default RangeWidget
