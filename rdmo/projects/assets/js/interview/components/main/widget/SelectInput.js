import React, { useState } from 'react'
import Select from 'react-select'
import AsyncSelect from 'react-select/async'
import CreatableSelect from 'react-select/creatable'
import CreatableAsyncSelect from 'react-select/async-creatable'

import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, isNil } from 'lodash'
import { useDebouncedCallback } from 'use-debounce'
// import { convert } from 'html-to-text'

import ProjectApi from '../../../api/ProjectApi'
import { projectId } from '../../../utils/meta'
import { isDefaultValue } from '../../../utils/value'
import { getValueOption } from '../../../utils/options'

import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'


const SelectInput = ({ question, value, options, disabled, creatable, updateValue, buttons }) => {

  const [inputValue, setInputValue] = useState('')

  const handleChange = (option) => {
    if (isNil(option)) {
      setInputValue('')
      updateValue(value, {})
    } else if (option.__isNew__ === true) {
      updateValue(value, {
        text: option.value,
        unit: question.unit,
        value_type: question.value_type
      })
    } else {
      if (option.has_provider) {
        updateValue(value, {
          external_id: option.id,
          text: option.text,
          unit: question.unit,
          value_type: question.value_type
        })
      } else {
        updateValue(value, {
          option: option.id,
          unit: question.unit,
          value_type: question.value_type
        })
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

  const valueOption = getValueOption(options, value)

  const isAsync = question.optionsets.some((optionset) => optionset.has_search)

  const selectProps = {
    key: value.id,
    classNamePrefix: 'react-select',
    className: classnames,
    backspaceRemovesValue: false,
    isDisabled: disabled,
    placeholder: gettext('Select ...'),
    noOptionsMessage: () => gettext('No options found'),
    loadingMessage: () => gettext('Loading ...'),
    options: options,
    value: valueOption,
    inputValue: inputValue,
    onInputChange: setInputValue,
    onChange: handleChange,
    getOptionValue: (option) => option.id,
    getOptionLabel: (option) => option.text,
    formatOptionLabel: (option) => (
      <span className="interview-select-option">
        <OptionText option={option} />
        <OptionHelp className="ml-10" option={option} />
      </span>
    )
  }

  return (
    <div className="interview-input">
      {
        creatable ? (
          isAsync ? (
            <CreatableAsyncSelect {...selectProps} loadOptions={handleLoadOptions} defaultOptions />
          ) : (
            <CreatableSelect {...selectProps} />
          )
        ) : (
          isAsync ? (
            <AsyncSelect {...selectProps} loadOptions={handleLoadOptions} defaultOptions />
          ) : (
            <Select {...selectProps} />
          )
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
  creatable: PropTypes.bool,
  updateValue: PropTypes.func.isRequired,
  buttons: PropTypes.node.isRequired
}

export default SelectInput
