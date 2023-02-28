import { getData } from '../utils/api'

class CoreApi {

  static fetchSettings() {
    return getData('/api/v1/core/settings/')
  }

  static fetchSites() {
    return getData('/api/v1/core/sites/')
  }

  static fetchGroups() {
    return getData('/api/v1/core/groups/')
  }

}

export default CoreApi
