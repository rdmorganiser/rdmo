import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class ConditionsApi {

  static fetchConditions(action) {
    let url = '/api/v1/conditions/conditions/'
    if (action == 'index') url += 'index/'
    return getData(url)
  }

  static fetchCondition(id) {
    return getData(`/api/v1/conditions/conditions/${id}/`)
  }

  static storeCondition(condition) {
    if (isNil(condition.id)) {
      return postData(`/api/v1/conditions/conditions/`, condition)
    } else {
      return putData(`/api/v1/conditions/conditions/${condition.id}/`, condition)
    }
  }

  static fetchRelations() {
    return getData('/api/v1/conditions/relations/')
  }

}

export default ConditionsApi
