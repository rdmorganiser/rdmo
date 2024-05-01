const gatherOptions = (question) => {
  return question.optionsets.reduce((options, optionset) => {
    return [
      ...options,
      ...optionset.options.map((option) => {
        option.has_provider = optionset.has_provider
        return option
      })
    ]
  }, [])
}

export { gatherOptions }
