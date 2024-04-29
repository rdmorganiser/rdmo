import React from 'react'
import PropTypes from 'prop-types'
import {  isNil } from 'lodash'

import { isDefaultValue } from '../../../../utils/value'

import QuestionAddValue from '../QuestionAddValue'
import QuestionDefault from '../QuestionDefault'
import QuestionEraseValue from '../QuestionEraseValue'
import QuestionRemoveValue from '../QuestionRemoveValue'

import RangeInput from './RangeInput'

const RangeWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {

  const handleCreateValue = (value) => {
    value.text = isNil(question.minimum) ? 0 : question.minimum
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
                {
                  isDefault && <QuestionDefault />
                }
                <QuestionEraseValue value={value} updateValue={updateValue} />
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
                isDefault={isDefault}
                updateValue={updateValue}
              />
            </div>
          )
        })
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
