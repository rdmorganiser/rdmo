import isNil from 'lodash/isNil'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ConditionsApi extends BaseApi {

  static fetchConditions(action) {
    let url = '/api/v1/conditions/conditions/'
    if (action == 'index') url += 'index/'
    return this.get(url)
  }

  static fetchCondition(id) {
    return this.get(`/api/v1/conditions/conditions/${id}/`)
  }

  static storeCondition(condition) {
    if (isNil(condition.id)) {
      return this.post('/api/v1/conditions/conditions/', condition)
    } else {
      return this.put(`/api/v1/conditions/conditions/${condition.id}/`, condition)
    }
  }

  static deleteCondition(question) {
    return this.delete(`/api/v1/conditions/conditions/${question.id}/`)
  }

  static fetchRelations() {
    return this.get('/api/v1/conditions/relations/')
  }

}

export default ConditionsApi
