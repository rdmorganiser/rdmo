import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class DomainApi {

  static fetchAttributes(index=false) {
    let url = '/api/v1/domain/attributes/'
    if (index) url += 'index/'
    return getData(url)
  }

  static fetchAttribute(id) {
    return getData(`/api/v1/domain/attributes/${id}/`)
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
