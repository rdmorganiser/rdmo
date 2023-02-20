import { getData } from 'rdmo/core/assets/js/utils/api'

class ManagementApi {

  static fetchMeta(index=false) {
    let url = '/api/v1/management/meta/'
    return getData(url)
  }

}

export default ManagementApi
