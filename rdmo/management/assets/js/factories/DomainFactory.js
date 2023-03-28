class QuestionsFactory {

  static createAttribute(config) {
    return {
      uri_prefix: config.settings.default_uri_prefix
    }
  }

}

export default QuestionsFactory
