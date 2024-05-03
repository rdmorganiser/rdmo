import React from 'react'
import PropTypes from 'prop-types'

import { isDefaultValue } from '../../../utils/value'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionDefault from '../question/QuestionDefault'
import QuestionError from '../question/QuestionError'
import QuestionRemoveValue from '../question/QuestionRemoveValue'

import TextareaInput from './TextareaInput'

const TextareaWidget = ({ question, values, currentSet, disabled, focus, createValue, updateValue, deleteValue }) => {
  return (
    <div className="interview-widgets">
      {
        values.map((value, valueIndex) => {
          const isDefault = isDefaultValue(question, value)

          return (
            <div key={valueIndex} className="interview-widget">
              <div className="options">
                <QuestionDefault isDefault={isDefault} />
                <QuestionRemoveValue
                  question={question}
                  values={values}
                  value={value}
                  disabled={disabled}
                  deleteValue={deleteValue}
                />
              </div>
              <TextareaInput
                value={value}
                disabled={disabled}
                isDefault={isDefault}
                updateValue={updateValue}
                focus={focus && valueIndex == values.length - 1}
              />
              <QuestionError value={value} />
            </div>
          )
        })
      }
      <QuestionAddValue
        question={question}
        values={values}
        currentSet={currentSet}
        disabled={disabled}
        createValue={createValue}
      />
    </div>
  )
}

TextareaWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  focus: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default TextareaWidget
