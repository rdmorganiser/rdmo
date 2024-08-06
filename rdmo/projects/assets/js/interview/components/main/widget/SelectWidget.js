import React from 'react'
import PropTypes from 'prop-types'

import { gatherOptions } from '../../../utils/options'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionDefault from '../question/QuestionDefault'
import QuestionEraseValue from '../question/QuestionEraseValue'
import QuestionError from '../question/QuestionError'
import QuestionSuccess from '../question/QuestionSuccess'
import QuestionRemoveValue from '../question/QuestionRemoveValue'

import SelectInput from './SelectInput'

const SelectWidget = ({ question, values, currentSet, disabled, creatable,
                        createValue, updateValue, deleteValue }) => {
  return (
    <div className="interview-widgets">
      {
        values.map((value, valueIndex) => {
          return (
            <div key={valueIndex} className="interview-widget">
              <SelectInput
                question={question}
                value={value}
                options={gatherOptions(question)}
                disabled={disabled}
                creatable={creatable}
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

SelectWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  creatable: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default SelectWidget
