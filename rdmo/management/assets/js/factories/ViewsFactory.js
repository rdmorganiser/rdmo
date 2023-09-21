class ViewsFactory {

  static createView(config) {
    return {
      model: 'views.view',
      uri_prefix: config.settings.default_uri_prefix,
      template: '{% load view_tags %}\n'
    }
  }

}

export default ViewsFactory
