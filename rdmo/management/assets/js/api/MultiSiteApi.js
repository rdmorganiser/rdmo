
import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class MultiSiteApi extends BaseApi {

  static UpdateElementAction(element, action) {
      const model_api_path = element.model.replace('.', '/').concat('s')
      let url = `/api/v1/${model_api_path}/${element.id}/${action}/`
      return this.put(url, element)
    }
  }
export default MultiSiteApi
