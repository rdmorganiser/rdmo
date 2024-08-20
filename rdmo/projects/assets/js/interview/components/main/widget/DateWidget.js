import React from 'react'
import PropTypes from 'prop-types'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionCopyValue from '../question/QuestionCopyValue'
import QuestionCopyValues from '../question/QuestionCopyValues'
import QuestionDefault from '../question/QuestionDefault'
import QuestionError from '../question/QuestionError'
import QuestionEraseValue from '../question/QuestionEraseValue'
import QuestionSuccess from '../question/QuestionSuccess'
import QuestionRemoveValue from '../question/QuestionRemoveValue'

import DateInput from './DateInput'

const DateWidget = ({ question, values, siblings, currentSet, disabled, createValue, updateValue, deleteValue, copyValue }) => {
  return (
    <div className="interview-widgets">
      {
        values.map((value, valueIndex) => {
          return (
            <div key={valueIndex} className="interview-widget">
              <DateInput
                question={question}
                value={value}
                disabled={disabled}
                updateValue={updateValue}
                buttons={
                  <div className="buttons">
                    <QuestionSuccess value={value}/>
                    <QuestionEraseValue value={value} disabled={disabled} updateValue={updateValue}/>
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
        createValue={createValue}
        copyValue={copyValue}
      />
      <QuestionCopyValues
        question={question}
        values={values}
        siblings={siblings}
        copyValue={copyValue}
      />
    </div>
  )
}

DateWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  siblings: PropTypes.array,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired,
  copyValue: PropTypes.func.isRequired
}

export default DateWidget
