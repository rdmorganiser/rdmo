import BaseApi from './BaseApi'

class CoreApi extends BaseApi {

  static fetchSettings() {
    return this.get('/api/v1/core/settings/')
  }

  static fetchSites() {
    return this.get('/api/v1/core/sites/')
  }

  static fetchGroups() {
    return this.get('/api/v1/core/groups/')
  }

}

export default CoreApi
