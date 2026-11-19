import { siteId } from 'rdmo/core/assets/js/utils/meta'

class QuestionsFactory {

  static createCatalog(settings) {
    return {
      model: 'questions.catalog',
      uri_prefix: settings.default_uri_prefix,
      available: true,
      sections: [],
      sites: settings.multisite ? [siteId] : [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

  static createSection(settings, parent) {
    return {
      model: 'questions.section',
      uri_prefix: settings.default_uri_prefix,
      uri_path: parent.catalog ? parent.catalog.uri_path : '',
      catalogs: parent.catalog ? [parent.catalog.id] : [],
      pages: [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

  static createPage(settings, parent) {
    return {
      model: 'questions.page',
      uri_prefix: settings.default_uri_prefix,
      uri_path: parent.section ? parent.section.uri_path : '',
      sections: parent.section ? [parent.section.id] : [],
      questionsets: [],
      questions: [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

  static createQuestionSet(settings, parent) {
    return {
      model: 'questions.questionset',
      uri_prefix: settings.default_uri_prefix,
      uri_path: parent.page ? parent.page.uri_path : (
        parent.questionset ? parent.questionset.uri_path : ''
      ),
      pages: parent.page ? [parent.page.id] : [],
      parents: parent.questionset ? [parent.questionset.id] : [],
      questionsets: [],
      questions: [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

  static createQuestion(settings, parent) {
    return {
      model: 'questions.question',
      uri_prefix: settings.default_uri_prefix,
      uri_path: parent.page ? parent.page.uri_path : (
        parent.questionset ? parent.questionset.uri_path : ''
      ),
      widget_type: 'text',
      value_type: 'text',
      pages: parent.page ? [parent.page.id] : [],
      questionsets: parent.questionset ? [parent.questionset.id] : [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

}

export default QuestionsFactory
