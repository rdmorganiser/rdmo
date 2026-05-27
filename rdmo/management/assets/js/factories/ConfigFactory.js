import { siteId } from 'rdmo/core/assets/js/utils/meta'

class ConfigFactory {

  static createPlugin(config) {
    return {
      model: 'config.plugin',
      uri_prefix: config.settings.default_uri_prefix,
      plugin_settings: {},
      available: true,
      sites: config.settings.multisite ? [siteId] : [],
      editors: config.settings.multisite ? [siteId] : []
    }
  }
}

export default ConfigFactory
