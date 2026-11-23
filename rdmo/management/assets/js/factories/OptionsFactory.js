import { siteId } from 'rdmo/core/assets/js/utils/meta'

class OptionsFactory {

  static createOptionSet(settings, parent) {
    return {
      model: 'options.optionset',
      uri_prefix: settings.default_uri_prefix,
      questions: parent.question ? [parent.question.id] : [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

  static createOption(settings, parent) {
    return {
      model: 'options.option',
      uri_prefix: settings.default_uri_prefix,
      uri_path: parent.optionset ? parent.optionset.uri_path : '',
      optionsets: parent.optionset ? [parent.optionset.id] : [],
      conditions: [],
      editors: settings.multisite ? [siteId] : [],
    }
  }

}

export default OptionsFactory
