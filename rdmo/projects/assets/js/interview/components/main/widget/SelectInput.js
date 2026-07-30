import React, { useEffect, useState } from 'react'
import Select from 'react-select'
import AsyncSelect from 'react-select/async'
import CreatableSelect from 'react-select/creatable'
import CreatableAsyncSelect from 'react-select/async-creatable'

import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isEmpty, isNil } from 'lodash'
import { useDebouncedCallback } from 'use-debounce'

import ProjectApi from '../../../api/ProjectApi'
import { projectId } from '../../../utils/meta'
import { getQuestionTextId, getQuestionHelpId } from '../../../utils/question'
import { isDefaultValue } from '../../../utils/value'
import { getValueOption } from '../../../utils/options'

import OptionHelp from './common/OptionHelp'
import OptionText from './common/OptionText'

import SelectValueContainer from './SelectValueContainer'

const SelectInput = ({ question, value, options, disabled, creatable, updateValue, buttons }) => {

  const [inputValue, setInputValue] = useState('')
  const [defaultValueOption, setDefaultValueOption] = useState(null)

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

  const loadOptions = (search, callback) => {
    // Updating "options" through the redux store is buggy, so we use AsyncSelect
    // and use a asynchronous callback to update the options in the select field.
    // Note that the "options" array in the component remains [].
    // This method is called either by handleLoadOptions when the user types in the async
    // component or by useEffect when the component is used with a default external_id.
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
  }

  const handleLoadOptions = useDebouncedCallback((searchText, callback) => {
    // use either the search text (typed by the user) or the text stored with the value
    // for when the select is opened.
    const search = searchText || value.text
    loadOptions(search, callback)
  }, 500)

  // handle default external ids by loading the options an set a default value option
  useEffect(() => {
    setDefaultValueOption(null)

    if (isEmpty(value.text) && !isNil(value.external_id) && isDefaultValue(question, value)) {
      let pending = true
      loadOptions(value.external_id, (loadedOptions) => {
        const option = loadedOptions.find((o) => o.id === value.external_id)
        if (pending && !isNil(option)) {
          value.text = option.text
          setDefaultValueOption(option)
        }
      })
      return () => { pending = false }
    }
  }, [value.id, value.external_id, value.text])

  const classnames = classNames({
    'react-select': true,
    'default': isDefaultValue(question, value)
  })

  const valueOption = defaultValueOption ?? getValueOption(options, value)

  const isAsync = question.optionsets.some((optionset) => optionset.has_search)

  const selectProps = {
    key: value.id,
    classNamePrefix: 'react-select',
    className: classnames,
    backspaceRemovesValue: false,
    isDisabled: disabled,
    placeholder: gettext('Select ...'),
    'aria-label': getQuestionTextId(question),
    'aria-description': getQuestionHelpId(question),
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
    ),
    components: { ValueContainer: SelectValueContainer }
  }

  return (
    <div className="interview-input select-input">
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
