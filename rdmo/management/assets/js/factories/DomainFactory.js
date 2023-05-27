class QuestionsFactory {

  static createAttribute(config, parent) {
    return {
      model: 'domain.attribute',
      uri_prefix: config.settings.default_uri_prefix,
      conditions: parent.condition ? [parent.condition.id] : [],
      pages: parent.page ? [parent.page.id] : [],
      questionsets: parent.questionset ? [parent.questionset.id] : [],
      questions: parent.question ? [parent.question.id] : []
    }
  }

}

export default QuestionsFactory
