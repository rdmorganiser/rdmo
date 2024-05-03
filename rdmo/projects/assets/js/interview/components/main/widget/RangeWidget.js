import React from 'react'
import PropTypes from 'prop-types'

import { isDefaultValue, initRange } from '../../../utils/value'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionDefault from '../question/QuestionDefault'
import QuestionError from '../question/QuestionError'
import QuestionEraseValue from '../question/QuestionEraseValue'
import QuestionRemoveValue from '../question/QuestionRemoveValue'

import RangeInput from './RangeInput'

const RangeWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {

  const handleCreateValue = (value) => {
    initRange(question, value)
    createValue(value)
  }

  return (
    <div className="interview-collection">
      {
        values.map((value, valueIndex) => {
          const isDefault = isDefaultValue(question, value)

          return (
            <div key={valueIndex} className="interview-input">
              <div className="interview-input-options">
                <QuestionDefault isDefault={isDefault} />
                <QuestionEraseValue value={value} disabled={disabled} updateValue={updateValue}/>
                <QuestionRemoveValue
                  question={question}
                  values={values}
                  value={value}
                  disabled={disabled}
                  deleteValue={deleteValue}
                />
              </div>
              <RangeInput
                value={value}
                minimum={question.minimum}
                maximum={question.maximum}
                step={question.step}
                disabled={disabled}
                isDefault={isDefault}
                updateValue={updateValue}
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
        createValue={handleCreateValue}
      />
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
