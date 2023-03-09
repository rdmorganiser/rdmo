import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class OptionsApi {

  static fetchOptionSets(action) {
    let url = '/api/v1/options/optionsets/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static fetchOptionSet(id, action) {
    let url = `/api/v1/options/optionsets/${id}/`
    if (action == 'nested') url += 'nested/'
    return getData(url)
  }

  static storeOptionSet(optionset) {
    if (isNil(optionset.id)) {
      return postData(`/api/v1/options/optionsets/`, optionset)
    } else {
      return putData(`/api/v1/options/optionsets/${optionset.id}/`, optionset)
    }
  }

  static fetchOptions(action) {
    let url = '/api/v1/options/options/'
    if (action == 'index') url += 'index/'
    return getData(url)
  }

  static fetchOption(id) {
    return getData(`/api/v1/options/options/${id}/`)
  }

  static storeOption(option) {
    if (isNil(option.id)) {
      return postData(`/api/v1/options/options/`, option)
    } else {
      return putData(`/api/v1/options/options/${option.id}/`, option)
    }
  }

  static fetchProviders() {
    return getData('/api/v1/options/providers/')
  }

}

export default OptionsApi
