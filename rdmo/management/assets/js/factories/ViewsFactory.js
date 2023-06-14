class ViewsFactory {

  static createView(config) {
    return {
      model: 'views.view',
      uri_prefix: config.settings.default_uri_prefix
    }
  }

}

export default ViewsFactory
