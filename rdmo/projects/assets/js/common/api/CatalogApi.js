import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class CatalogApi extends BaseApi {
  static fetchCatalogs() {
    return this.get('/api/v1/projects/catalogs/')
  }
}

export default CatalogApi
