class QuestionsFactory {

  static createCatalog(config) {
    return {
      model: 'questions.catalog',
      uri_prefix: config.settings.default_uri_prefix,
      available: true,
      sections: [],
      sites: config.settings.multisite ? [config.currentSite.id] : [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

  static createSection(config, parent) {
    return {
      model: 'questions.section',
      uri_prefix: config.settings.default_uri_prefix,
      uri_path: parent.catalog ? `${parent.catalog.uri_path}/`: '',
      catalogs: parent.catalog ? [parent.catalog.id] : [],
      pages: [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

  static createPage(config, parent) {
    return {
      model: 'questions.page',
      uri_prefix: config.settings.default_uri_prefix,
      uri_path: parent.section ? `${parent.section.uri_path}/`: '',
      sections: parent.section ? [parent.section.id] : [],
      questionsets: [],
      questions: [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

  static createQuestionSet(config, parent) {
    return {
      model: 'questions.questionset',
      uri_prefix: config.settings.default_uri_prefix,
      uri_path: parent.page ? `${parent.page.uri_path}/`: (
        parent.questionset ? `${parent.questionset.uri_path}/`: ''
      ),
      pages: parent.page ? [parent.page.id] : [],
      parents: parent.questionset ? [parent.questionset.id] : [],
      questionsets: [],
      questions: [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

  static createQuestion(config, parent) {
    return {
      model: 'questions.question',
      uri_prefix: config.settings.default_uri_prefix,
      uri_path: parent.page ? `${parent.page.uri_path}/`: (
        parent.questionset ? `${parent.questionset.uri_path}/`: ''
      ),
      widget_type: 'text',
      value_type: 'text',
      pages: parent.page ? [parent.page.id] : [],
      questionsets: parent.questionset ? [parent.questionset.id] : [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

}

export default QuestionsFactory
