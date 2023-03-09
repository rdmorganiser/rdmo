import { getData } from 'rdmo/core/assets/js/utils/api'

class ManagementApi {

  static fetchMeta() {
    return getData('/api/v1/management/meta/')
  }

}

export default ManagementApi
