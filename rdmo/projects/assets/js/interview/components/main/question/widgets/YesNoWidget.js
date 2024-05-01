import React from 'react'
import PropTypes from 'prop-types'

import { isDefaultValue } from '../../../../utils/value'

import QuestionAddValue from '../QuestionAddValue'
import QuestionDefault from '../QuestionDefault'
import QuestionError from '../QuestionError'
import QuestionEraseValue from '../QuestionEraseValue'
import QuestionRemoveValue from '../QuestionRemoveValue'

import YesNoInput from './YesNoInput'

const YesNoWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
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
              <YesNoInput
                value={value}
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
        createValue={createValue}
      />
    </div>
  )
}

YesNoWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default YesNoWidget
