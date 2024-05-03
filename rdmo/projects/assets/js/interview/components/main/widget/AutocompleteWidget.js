import React from 'react'
import PropTypes from 'prop-types'

import { isDefaultValue } from '../../../utils/value'
import { gatherOptions } from '../../../utils/options'

import QuestionAddValue from '../question/QuestionAddValue'
import QuestionDefault from '../question/QuestionDefault'
import QuestionError from '../question/QuestionError'
import QuestionRemoveValue from '../question/QuestionRemoveValue'

import AutocompleteInput from './AutocompleteInput'

const AutocompleteWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
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
              <AutocompleteInput
                value={value}
                options={gatherOptions(question)}
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

AutocompleteWidget.propTypes = {
  question: PropTypes.object.isRequired,
  values: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  currentSet: PropTypes.object.isRequired,
  createValue: PropTypes.func.isRequired,
  updateValue: PropTypes.func.isRequired,
  deleteValue: PropTypes.func.isRequired
}

export default AutocompleteWidget
