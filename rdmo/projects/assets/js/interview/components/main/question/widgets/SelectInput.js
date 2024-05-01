import React, { useState, useEffect } from 'react'
import ReactSelect from 'react-select'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isNil } from 'lodash'

import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'

const SelectInput = ({ value, options, disabled, isDefault, updateValue }) => {
  const selectOptions = options.map(option => ({
    value: option,
    label: option.text
  }))

  const [inputValue, setInputValue] = useState('')
  useEffect(() => {
    setInputValue(selectOptions.find((selectOption) => (
      selectOption.value.has_provider ? (value.external_id === selectOption.value.id)
                                      : (value.option === selectOption.value.id)
    )))
  }, [value.id, value.option, value.external_id])

  const handleChange = (selectedOption) => {
    if (isNil(selectedOption)) {
      updateValue(value, {})
    } else {
      if (selectedOption.value.has_provider) {
        updateValue(value, { external_id: selectedOption.value.id, text: selectedOption.value.text })
      } else {
        updateValue(value, { option: selectedOption.value.id })
      }
    }
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
      formatOptionLabel={({ value }) => (
        <span>
          <OptionText option={value} />
          <OptionHelp className="ml-10" option={value} />
        </span>
      )}
    />
  )
}

SelectInput.propTypes = {
  value: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  isDefault: PropTypes.bool,
  updateValue: PropTypes.func.isRequired
}

export default SelectInput
