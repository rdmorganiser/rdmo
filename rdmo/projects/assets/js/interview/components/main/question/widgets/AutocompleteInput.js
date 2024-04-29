import React, { useState, useEffect } from 'react'
import ReactSelect from 'react-select'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isNil } from 'lodash'

const AutocompleteInput = ({ value, options, disabled, isDefault, updateValue }) => {
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

  const classnames = classNames({
    'react-select': true,
    'default': isDefault
  })

  return (
    <ReactSelect
      classNamePrefix="react-select"
      className={classnames}
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
  isDefault: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

export default AutocompleteInput
