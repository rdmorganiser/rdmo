class ConditionsFactory {

  static createCondition(config) {
    return {
      uri_prefix: config.settings.default_uri_prefix
    }
  }

}

export default ConditionsFactory
