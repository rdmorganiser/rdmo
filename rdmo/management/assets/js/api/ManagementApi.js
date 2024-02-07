import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ManagementApi extends BaseApi {

  static fetchMeta() {
    return this.get('/api/v1/management/meta/')
  }

  static uploadFile(file) {
    return this.upload('/api/v1/management/upload/', file)
  }

  static importElements(elements) {
    return this.post('/api/v1/management/import/', { elements })
  }

}

export default ManagementApi
