class ConditionsFactory {

  static createCondition(config, parent) {
    return {
      model: 'conditions.condition',
      uri_prefix: config.settings.default_uri_prefix,
      relation: 'eq',
      optionsets: parent.optionset ? [parent.optionset.id] : [],
      pages: parent.page ? [parent.page.id] : [],
      questionsets: parent.questionset ? [parent.questionset.id] : [],
      questions: parent.question ? [parent.question.id] : [],
      tasks: parent.task ? [parent.task.id] : [],
      editors: config.settings.multisite ? [config.currentSite.id] : [],
    }
  }

}

export default ConditionsFactory
