import { getData } from 'rdmo/core/assets/js/utils/api'

class DomainApi {

  static fetchAttributes(index=false) {
    let url = '/api/v1/domain/attributes/'
    if (index) url += 'index/'
    return getData(url)
  }

}

export default DomainApi
