import { siteId } from 'rdmo/core/assets/js/utils/meta'

class ViewsFactory {

  static createView(config) {
    return {
      model: 'views.view',
      uri_prefix: config.settings.default_uri_prefix,
      template: '{% load view_tags %}\n',
      sites:  config.settings.multisite ? [siteId] : [],
      editors:  config.settings.multisite ? [siteId] : [],
    }
  }

}

export default ViewsFactory
