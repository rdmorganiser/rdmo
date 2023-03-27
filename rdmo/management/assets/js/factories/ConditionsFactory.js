class ConditionsFactory {

  static createCondition(config) {
    return {
      uri_prefix: config.default_uri_prefix
    }
  }

}

export default ConditionsFactory
