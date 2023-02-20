import { getData } from 'rdmo/core/assets/js/utils/api'

class ConditionApi {

  static fetchConditions(index=false) {
    let url = '/api/v1/conditions/conditions/'
    if (index) url += 'index/'
    return getData(url)
  }

}

export default ConditionApi
