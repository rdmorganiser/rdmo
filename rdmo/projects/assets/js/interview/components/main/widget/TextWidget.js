import React from 'react'
import PropTypes from 'prop-types'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionCopyValue from '../question/QuestionCopyValue'
import QuestionCopyValues from '../question/QuestionCopyValues'
import QuestionDefault from '../question/QuestionDefault'
import QuestionError from '../question/QuestionError'
import QuestionReuseValue from '../question/QuestionReuseValue'
import QuestionRemoveValue from '../question/QuestionRemoveValue'
import QuestionSuccess from '../question/QuestionSuccess'

import TextInput from './TextInput'

const TextWidget = ({ page, question, sets, values, siblings, currentSet, disabled,
                      createValue, updateValue, deleteValue, copyValue }) => {
  return (
    <div className="interview-widgets">
      {
        values.map((value, valueIndex) => {
          return (
            <div key={valueIndex} className="interview-widget">
              <TextInput
                question={question}
                value={value}
                disabled={disabled}
                updateValue={updateValue}
                buttons={
                  <div className="buttons">
                    <QuestionSuccess value={value}/>
                    <QuestionReuseValue
                      page={page}
                      question={question}
                      value={value}
                      disabled={disabled}
                      updateValue={updateValue}
                    />
                    <QuestionCopyValue question={question} value={value} siblings={siblings} copyValue={copyValue} />
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

TextWidget.propTypes = {
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

export default TextWidget
