import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'

import AddValue from './common/AddValue'
import RemoveValue from './common/RemoveValue'

const YesNoInput = ({ value, disabled, updateValue }) => {
  const [inputValue, setInputValue] = useState('')
  useEffect(() => {setInputValue(value.text)}, [value.id])

  const handleChange = (value, text) => {
    updateValue(value, { text })
  }

  return (
    <div className="radio-control">
      <div className="radio yesno">
        <label>
            <input
              type="radio"
              value="1"
              disabled={disabled}
              checked={inputValue == '1'}
              onChange={(event) => {
                setInputValue(event.target.value)
                handleChange(value, event.target.value)
              }} />
            <span>{gettext('Yes')}</span>
        </label>
        <label>
            <input
              type="radio"
              value="0"
              checked={inputValue == '0'}
              disabled={disabled}
              onChange={(event) => {
                setInputValue(event.target.value)
                handleChange(value, event.target.value)
              }} />
            <span>{gettext('No')}</span>
        </label>
      </div>
    </div>
  )
}

YesNoInput.propTypes = {
  value: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

const YesNoWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
  return (
    <div className="interview-collection">
      {
        values.map((value, valueIndex) => (
          <div key={valueIndex} className="interview-input">
            <div className="interview-input-options">
              {
                question.is_collection && <RemoveValue value={value} deleteValue={deleteValue} />
              }
            </div>
            <YesNoInput
              value={value}
              disabled={disabled}
              updateValue={updateValue}
            />
          </div>
        ))
      }
      {
        question.is_collection && (
          <AddValue question={question} values={values} currentSet={currentSet} createValue={createValue} />
        )
      }
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
