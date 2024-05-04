import React from 'react'
import PropTypes from 'prop-types'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionDefault from '../question/QuestionDefault'
import QuestionError from '../question/QuestionError'
import QuestionEraseValue from '../question/QuestionEraseValue'
import QuestionRemoveValue from '../question/QuestionRemoveValue'

import DateInput from './DateInput'

const DateWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
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
                    <QuestionEraseValue value={value} disabled={disabled} updateValue={updateValue}/>
                    <QuestionRemoveValue
                      question={question}
                      values={values}
                      value={value}
                      disabled={disabled}
                      deleteValue={deleteValue}
                    />
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
      />
    </div>
  )
}

DateWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default DateWidget
