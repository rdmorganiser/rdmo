import React, { useState } from 'react'
import Select from 'react-select'
import AsyncSelect from 'react-select/async'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, isNil } from 'lodash'
import { useDebouncedCallback } from 'use-debounce'
import { convert } from 'html-to-text'

import ProjectApi from '../../../api/ProjectApi'
import projectId from '../../../utils/projectId'
import { isDefaultValue } from '../../../utils/value'

import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'


const SelectInput = ({ question, value, options, disabled, async, updateValue, buttons }) => {

  const [inputValue, setInputValue] = useState('')
  const [isOpen, setIsOpen] = useState(false)

  const handleChange = (option) => {
    if (isNil(option)) {
      setIsOpen(false)  // close the select input when the value is reset
      setInputValue('')
      updateValue(value, {})
    } else {
      if (option.has_provider) {
        updateValue(value, { external_id: option.id, text: option.text })
      } else {
        updateValue(value, { option: option.id })
      }
    }
  }

  const handleLoadOptions = useDebouncedCallback((searchText, callback) => {
    // Updating "options" through the redux store is buggy, so we use AsyncSelect
    // and use a asyncrounous callback to update the options in the select field.
    // Note that the "options" array in the component remains [].
    const search = searchText || value.text
    if (isEmpty(search)) {
      callback([])
    } else {
      Promise.all(question.optionsets.map((optionset) => {
        return ProjectApi.fetchOptions(projectId, optionset.id, search)
      })).then((results) => {
        const options = results.reduce((selectOptions, options) => {
          return [...selectOptions, ...options.map(option => ({...option, has_provider: true}))]
        }, [])

        callback(options)
      })
    }
  }, 500)

  const classnames = classNames({
    'react-select': true,
    'default': isDefaultValue(question, value)
  })

  const selectedOption = (isEmpty(options) && !isEmpty(value.external_id)) ? (
    // if an external id is set but no options are retrived yet, we faka an option with
    // the stored value, so that it is displayed before the input is opened
    {
      id: value.external_id || value.option,
      text: value.text
    }
  ) : options.find((option) => (
    option.has_provider ? option.id === value.external_id : option.id === value.option
  ))

  const selectProps = {
    classNamePrefix: 'react-select',
    className: classnames,
    backspaceRemovesValue: false,
    isClearable: true,
    isDisabled: disabled,
    placeholder: gettext('Select ...'),
    noOptionsMessage: () => gettext('No options found'),
    loadingMessage: () => gettext('Loading ...'),
    options: options,
    value: selectedOption,
    inputValue: inputValue,
    onInputChange: setInputValue,
    onChange: handleChange,
    clearValue: () => {
      console.log('lol')
    },
    menuIsOpen: isOpen,
    onMenuOpen: () => {
      setIsOpen(true)

      // replace the text shown in the select input with a plain text version
      if (selectedOption) {
        setInputValue(convert(selectedOption.text))
      }
    },
    onMenuClose: () => setIsOpen(false),
    getOptionValue: (option) => option.id,
    getOptionLabel: (option) => option.text,
    formatOptionLabel: (option) => (
      <span>
        <OptionText option={option} />
        <OptionHelp className="ml-10" option={option} />
      </span>
    )
  }

  return (
    <div className="interview-input">
      {
        async ? (
          <AsyncSelect {...selectProps} loadOptions={handleLoadOptions} defaultOptions />
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
