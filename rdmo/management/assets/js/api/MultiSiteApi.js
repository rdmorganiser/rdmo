
import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class MultiSiteApi extends BaseApi {

  static UpdateElementAction(element, action) {
      const model_api_path = element.model.replace('.', '/').concat('s')
      let url = `/api/v1/${model_api_path}/${element.id}/${action}/`
      console.log('UpdateElementAction', url, element, action, this)
      return this.put(url, element)
    }
  }
export default MultiSiteApi
