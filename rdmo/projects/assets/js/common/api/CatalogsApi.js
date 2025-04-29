import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class CatalogsApi extends BaseApi {
  static fetchCatalogs() {
    return fetch('/api/v1/projects/catalogs/').then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error(response.statusText)
      }
    })
  }
}

export default CatalogsApi
