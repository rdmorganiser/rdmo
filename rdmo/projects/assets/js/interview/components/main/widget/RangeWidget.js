import React from 'react'
import PropTypes from 'prop-types'

import { initRange } from '../../../utils/value'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionCopyValue from '../question/QuestionCopyValue'
import QuestionCopyValues from '../question/QuestionCopyValues'
import QuestionDefault from '../question/QuestionDefault'
import QuestionEraseValue from '../question/QuestionEraseValue'
import QuestionError from '../question/QuestionError'
import QuestionRemoveValue from '../question/QuestionRemoveValue'
import QuestionReuseValue from '../question/QuestionReuseValue'
import QuestionSuccess from '../question/QuestionSuccess'

import RangeInput from './RangeInput'

const RangeWidget = ({ page, question, sets, values, siblings, currentSet, disabled,
                       createValue, updateValue, deleteValue, copyValue }) => {

  const handleCreateValue = (value) => {
    initRange(question, value)
    createValue(value)
  }

  const handleEraseValue = (value, attrs) => {
    initRange(question, attrs)
    updateValue(value, attrs)
  }

  return (
    <div className="interview-widgets">
      {
        values.map((value, valueIndex) => {
          return (
            <div key={valueIndex} className="interview-widget">
              <RangeInput
                question={question}
                value={value}
                disabled={disabled}
                updateValue={updateValue}
                buttons={
                  <div className="buttons">
                    <QuestionSuccess value={value}/>
                    <QuestionReuseValue page={page} value={value} updateValue={updateValue}/>
                    <QuestionEraseValue value={value} disabled={disabled} updateValue={handleEraseValue}/>
                    <QuestionRemoveValue
                      question={question}
                      values={values}
                      value={value}
                      disabled={disabled}
                      deleteValue={deleteValue}
                    />
                    <QuestionCopyValue question={question} value={value} siblings={siblings} copyValue={copyValue} />
                    <QuestionDefault question={question} value={value} />
                  </div>
                }
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
        copyValue={copyValue}
      />
      <QuestionCopyValues
        question={question}
        sets={sets}
        values={values}
        siblings={siblings}
        currentSet={currentSet}
        copyValue={copyValue}
      />
    </div>
  )
}

RangeWidget.propTypes = {
  page: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired,
  copyValue: PropTypes.func.isRequired
}

export default RangeWidget
