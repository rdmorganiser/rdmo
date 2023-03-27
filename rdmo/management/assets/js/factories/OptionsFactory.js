class OptionsFactory {

  static createOptionSet(config) {
    return {
      uri_prefix: config.default_uri_prefix
    }
  }

  static createOption(config, parent) {
    return {
      uri_prefix: config.default_uri_prefix,
      optionsets: parent.optionset ? [parent.optionset.id] : [],
      conditions: []
    }
  }

}

export default OptionsFactory
