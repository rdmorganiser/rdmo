import React from 'react'
import PropTypes from 'prop-types'

import { isDefaultValue } from '../../../../utils/value'

import QuestionAddValue from '../QuestionAddValue'
import QuestionDefault from '../QuestionDefault'
import QuestionRemoveValue from '../QuestionRemoveValue'

import SelectInput from './SelectInput'

const SelectWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
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
                {
                  (question.is_collection || values.length > 1) && (
                    <QuestionRemoveValue value={value} deleteValue={deleteValue} />
                  )
                }
              </div>
              <SelectInput
                value={value}
                options={question.options}
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
          <QuestionAddValue question={question} values={values} currentSet={currentSet} createValue={createValue} />
        )
      }
    </div>
  )
}

SelectWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default SelectWidget
