class ViewsFactory {

  static createView(config) {
    return {
      uri_prefix: config.settings.default_uri_prefix
    }
  }

}

export default ViewsFactory
