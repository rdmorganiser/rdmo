import { get, isEmpty, isNil } from 'lodash'

const checkOptionSet = (optionset, set) => {
  return !optionset.has_conditions || get(set, `optionsets.${optionset.id}`)
}

const gatherOptions = (question, set) => {
  return question.optionsets.reduce((options, optionset) => {
    if (checkOptionSet(optionset, set)) {
      return [
        ...options,
        ...optionset.options.map((option) => {
          option.has_provider = optionset.has_provider
          return option
        })
      ]
    } else {
      // the condition for this optionset and set resolved false
      return options
    }
  }, [])
}

const updateOptions = (page, optionset, options) => {
  page.optionsets.forEach((pageOptionset) => {
    if (pageOptionset.id == optionset.id) {
      optionset.options = options
    }
  })
}

const getValueOption = (options, value) => {
  if (!isNil(value.option)) {
    // this is a value referencing a regular option
    return options.find((option) => (option.id === value.option))
  } else if (!isEmpty(value.external_id)) {
    // this is a value with an external id from a provider
    if (isEmpty(options)) {
      // if an external id is set but no options are retrived yet, we fake an option with
      // the stored value, so that it is displayed before the input is opened
      return {
        id: value.external_id,
        text: value.text
      }
    } else {
      return options.find((option) => (option.id === value.external_id))
    }
  } else if (!isEmpty(value.text)) {
    // this is a value without an option (free autocomplete), so we fake an option without an id
    return {
      id: null,
      text: value.text
    }
  } else {
    // this is an empty value
    return null
  }
}

export { gatherOptions, updateOptions, getValueOption }
