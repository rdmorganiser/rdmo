import { siteId } from 'rdmo/core/assets/js/utils/meta'

class ViewsFactory {

  static createView(settings) {
    return {
      model: 'views.view',
      uri_prefix: settings.default_uri_prefix,
      template: '{% load view_tags %}\n',
      sites:  settings.multisite ? [siteId] : [],
      editors:  settings.multisite ? [siteId] : [],
    }
  }

}

export default ViewsFactory
