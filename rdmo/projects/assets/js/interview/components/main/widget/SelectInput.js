import React, { useState, useEffect } from 'react'
import Select from 'react-select'
import AsyncSelect from 'react-select/async'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, isNil } from 'lodash'
import { useDebouncedCallback } from 'use-debounce'

import ProjectApi from '../../../api/ProjectApi'
import projectId from '../../../utils/projectId'
import { isDefaultValue } from '../../../utils/value'

import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'


const SelectInput = ({ question, value, options, disabled, async, updateValue, buttons }) => {

  const selectOptions = options.map(option => ({
    value: option,
    label: option.text
  }))

  const [inputValue, setInputValue] = useState('')
  const [placeholder, setPlaceholder] = useState('')

  useEffect(() => {
    const inputValue = selectOptions.find((selectOption) => (
      selectOption.value.has_provider ? (value.external_id === selectOption.value.id)
                                      : (value.option === selectOption.value.id)
    ))

    if (value.external_id) {
      setPlaceholder(value.text)
      setInputValue(inputValue)
    } else if (value.option) {
      setPlaceholder(gettext('Select ...'))
      setInputValue(inputValue)
    } else {
      setPlaceholder(gettext('Select ...'))
    }

  }, [value.id, value.option, value.external_id, options])

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

  const handleLoadOptions = useDebouncedCallback((searchText, callback) => {
    if (isEmpty(searchText)) {
      callback([])
    } else {
      Promise.all(question.optionsets.map((optionset) => {
        return ProjectApi.fetchOptions(projectId, optionset.id, searchText)
      })).then((results) => {
        const selectOptions = results.reduce((selectOptions, options) => {
          return [...selectOptions, ...options.map(option => ({
            value: {...option, has_provider: true},
            label: option.text
          }))]
        }, [])

        callback(selectOptions)
      })
    }
  }, 500)

  const classnames = classNames({
    'react-select': true,
    'default': isDefaultValue(question, value)
  })

  const selectProps = {
    classNamePrefix: 'react-select',
    className: classnames,
    isClearable: true,
    options: selectOptions,
    value: inputValue,
    onChange: (option) => {
      setInputValue(option)
      handleChange(option)
    },
    isDisabled: disabled,
    formatOptionLabel: ({ value }) => (
      <span>
        <OptionText option={value} />
        <OptionHelp className="ml-10" option={value} />
      </span>
    ),
    placeholder: placeholder
  }

  return (
    <div className="interview-input">
      {
        async ? (
          <AsyncSelect {...selectProps} loadOptions={handleLoadOptions} />
        ) : (
          <Select {...selectProps} />
        )
      }
      {buttons}
    </div>
  )
}

SelectInput.propTypes = {
  question: PropTypes.object.isRequired,
  value: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  disabled: PropTypes.bool,
  async: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default SelectInput
