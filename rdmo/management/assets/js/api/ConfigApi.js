import isNil from 'lodash/isNil'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ConfigApi extends BaseApi {

  static fetchPlugins(action) {
    let url = '/api/v1/config/plugins/'
    if (action == 'index') url += 'index/'
    return this.get(url)
  }

  static fetchPlugin(id) {
    return this.get(`/api/v1/config/plugins/${id}/`)
  }

  static storePlugin(plugin, action) {
    if (isNil(plugin.id)) {
      return this.post('/api/v1/config/plugins/', plugin)
    } else {
      const actionPath = isNil(action) ? '' : `${action}/`
      return this.put(`/api/v1/config/plugins/${plugin.id}/${actionPath}`, plugin)
    }
  }

  static deletePlugin(plugin) {
    return this.delete(`/api/v1/config/plugins/${plugin.id}/`)
  }
}

export default ConfigApi
