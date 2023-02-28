import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class OptionsApi {

  static fetchOptionSets(index=false, nested=false) {
    let url = '/api/v1/options/optionsets/'
    if (index) url += 'index/'
    if (nested) url += 'nested/'
    return getData(url)
  }

  static fetchOptionSet(id) {
    return getData(`/api/v1/options/optionsets/${id}/`)
  }

  static storeOptionSet(optionset) {
    if (isNil(optionset.id)) {
      return postData(`/api/v1/options/optionsets/`, optionset)
    } else {
      return putData(`/api/v1/options/optionsets/${optionset.id}/`, optionset)
    }
  }

  static fetchOptions(index=false) {
    let url = '/api/v1/options/options/'
    if (index) url += 'index/'
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
