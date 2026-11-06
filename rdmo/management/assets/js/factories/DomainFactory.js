import { siteId } from 'rdmo/core/assets/js/utils/meta'

class DomainFactory {

  static createAttribute(settings, parent) {
    return {
      model: 'domain.attribute',
      uri_prefix: settings.default_uri_prefix,
      parent: parent.attribute ? parent.attribute.id : null,
      conditions: parent.condition ? [parent.condition.id] : [],
      pages: parent.page ? [parent.page.id] : [],
      questionsets: parent.questionset ? [parent.questionset.id] : [],
      questions: parent.question ? [parent.question.id] : [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

}

export default DomainFactory
