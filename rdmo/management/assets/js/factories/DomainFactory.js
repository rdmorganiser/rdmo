class QuestionsFactory {

  static createAttribute(config) {
    return {
      uri_prefix: config.default_uri_prefix
    }
  }

}

export default QuestionsFactory
