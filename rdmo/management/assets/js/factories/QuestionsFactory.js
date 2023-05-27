class QuestionsFactory {

  static createCatalog(config) {
    return {
      model: 'questions.catalog',
      uri_prefix: config.settings.default_uri_prefix,
      available: true,
      sections: []
    }
  }

  static createSection(config, parent) {
    return {
      model: 'questions.section',
      uri_prefix: config.settings.default_uri_prefix,
      catalogs: parent.catalog ? [parent.catalog.id] : [],
      pages: []
    }
  }

  static createPage(config, parent) {
    return {
      model: 'questions.page',
      uri_prefix: config.settings.default_uri_prefix,
      sections: parent.section ? [parent.section.id] : [],
      questionsets: [],
      questions: []
    }
  }

  static createQuestionSet(config, parent) {
    return {
      model: 'questions.questionset',
      uri_prefix: config.settings.default_uri_prefix,
      pages: parent.page ? [parent.page.id] : [],
      parents: parent.questionset ? [parent.questionset.id] : [],
      questionsets: [],
      questions: []
    }
  }

  static createQuestion(config, parent) {
    return {
      model: 'questions.question',
      uri_prefix: config.settings.default_uri_prefix,
      widget_type: 'text',
      value_type: 'text',
      pages: parent.page ? [parent.page.id] : [],
      questionsets: parent.questionset ? [parent.questionset.id] : []
    }
  }

}

export default QuestionsFactory
