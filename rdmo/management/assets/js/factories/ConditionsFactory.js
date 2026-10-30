import { siteId } from 'rdmo/core/assets/js/utils/meta'

class ConditionsFactory {

  static createCondition(settings, parent) {
    return {
      model: 'conditions.condition',
      uri_prefix: settings.default_uri_prefix,
      relation: 'eq',
      optionsets: parent.optionset ? [parent.optionset.id] : [],
      pages: parent.page ? [parent.page.id] : [],
      questionsets: parent.questionset ? [parent.questionset.id] : [],
      questions: parent.question ? [parent.question.id] : [],
      tasks: parent.task ? [parent.task.id] : [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

}

export default ConditionsFactory
