import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import ReactSelect from 'react-select'
import { isNil } from 'lodash'

import AddValue from './common/AddValue'
import RemoveValue from './common/RemoveValue'

const AutocompleteInput = ({ value, options, disabled, updateValue }) => {
  const selectOptions = options.map(option => ({
    value: option.id,
    label: option.text
  }))

  const [inputValue, setInputValue] = useState('')
  useEffect(() => {
    setInputValue(selectOptions.find((selectOption) => selectOption.value == value.option))
  }, [value.id, value.option])

  const handleChange = (selectedOption) => {
    updateValue(value, {
      option: isNil(selectedOption) ? null : selectedOption.value
    })
  }

  return (
    <ReactSelect
      classNamePrefix="react-select"
      className="react-select"
      isClearable={true}
      options={selectOptions}
      value={inputValue}
      onChange={(option) => {
        setInputValue(option)
        handleChange(option)
      }}
      isDisabled={disabled}
    />
  )
}

AutocompleteInput.propTypes = {
  value: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

const AutocompleteWidget = ({ question, values, currentSet, disabled, createValue, updateValue, deleteValue }) => {
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
            <AutocompleteInput
              value={value}
              options={question.options}
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
