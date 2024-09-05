class OptionsFactory {

  static createOptionSet(config, parent) {
    return {
      model: 'options.optionset',
      uri_prefix: config.settings.default_uri_prefix,
      questions: parent.question ? [parent.question.id] : [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

  static createOption(config, parent) {
    return {
      model: 'options.option',
      uri_prefix: config.settings.default_uri_prefix,
      uri_path: parent.optionset ? parent.optionset.uri_path : '',
      optionsets: parent.optionset ? [parent.optionset.id] : [],
      conditions: [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

}

export default OptionsFactory
