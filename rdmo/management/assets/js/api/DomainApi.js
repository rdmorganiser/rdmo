import isNil from 'lodash/isNil'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class DomainApi extends BaseApi {

  static fetchAttributes(action) {
    let url = '/api/v1/domain/attributes/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static fetchAttribute(id, action) {
    let url = `/api/v1/domain/attributes/${id}/`
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static storeAttribute(attribute) {
    if (isNil(attribute.id)) {
      return this.post('/api/v1/domain/attributes/', attribute)
    } else {
      return this.put(`/api/v1/domain/attributes/${attribute.id}/`, attribute)
    }
  }

  static deleteAttribute(attribute) {
    return this.delete(`/api/v1/domain/attributes/${attribute.id}/`)
  }

}

export default DomainApi
