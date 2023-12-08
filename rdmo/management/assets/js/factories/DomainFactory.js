class DomainFactory {

  static createAttribute(config, parent) {
    return {
      model: 'domain.attribute',
      uri_prefix: config.settings.default_uri_prefix,
      parent: parent.attribute ? parent.attribute.id : null,
      conditions: parent.condition ? [parent.condition.id] : [],
      pages: parent.page ? [parent.page.id] : [],
      questionsets: parent.questionset ? [parent.questionset.id] : [],
      questions: parent.question ? [parent.question.id] : [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

}

export default DomainFactory
