class OptionsFactory {

  static createOptionSet(config, parent) {
    return {
      model: 'options.optionset',
      uri_prefix: config.settings.default_uri_prefix,
      questions: parent.question ? [parent.question.id] : []
    }
  }

  static createOption(config, parent) {
    return {
      model: 'options.option',
      uri_prefix: config.settings.default_uri_prefix,
      optionsets: parent.optionset ? [parent.optionset.id] : [],
      conditions: []
    }
  }

}

export default OptionsFactory
