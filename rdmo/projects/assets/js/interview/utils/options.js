import { get } from 'lodash'

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

export { gatherOptions }
