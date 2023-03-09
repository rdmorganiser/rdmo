import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class DomainApi {

  static fetchAttributes(action) {
    let url = '/api/v1/domain/attributes/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static fetchAttribute(id, action) {
    let url = `/api/v1/domain/attributes/${id}/`
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static storeAttribute(attribute) {
    if (isNil(attribute.id)) {
      return postData(`/api/v1/domain/attributes/`, attribute)
    } else {
      return putData(`/api/v1/domain/attributes/${attribute.id}/`, attribute)
    }
  }

}

export default DomainApi
