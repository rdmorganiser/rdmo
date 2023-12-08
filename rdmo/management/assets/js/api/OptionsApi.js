import isNil from 'lodash/isNil'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class OptionsApi extends BaseApi {

  static fetchOptionSets(action) {
    let url = '/api/v1/options/optionsets/'
    if (action == 'index') url += 'index/'
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static fetchOptionSet(id, action) {
    let url = `/api/v1/options/optionsets/${id}/`
    if (action == 'nested') url += 'nested/'
    return this.get(url)
  }

  static storeOptionSet(optionset) {
    if (isNil(optionset.id)) {
      return this.post('/api/v1/options/optionsets/', optionset)
    } else {
      return this.put(`/api/v1/options/optionsets/${optionset.id}/`, optionset)
    }
  }

  static deleteOptionSet(optionset) {
    return this.delete(`/api/v1/options/optionsets/${optionset.id}/`)
  }

  static fetchOptions(action) {
    let url = '/api/v1/options/options/'
    if (action == 'index') url += 'index/'
    return this.get(url)
  }

  static fetchOption(id) {
    return this.get(`/api/v1/options/options/${id}/`)
  }

  static storeOption(option) {
    if (isNil(option.id)) {
      return this.post('/api/v1/options/options/', option)
    } else {
      return this.put(`/api/v1/options/options/${option.id}/`, option)
    }
  }

  static deleteOption(option) {
    return this.delete(`/api/v1/options/options/${option.id}/`)
  }

  static fetchAdditionalInputs() {
    return this.get('/api/v1/options/additionalinputs/')
  }

  static fetchProviders() {
    return this.get('/api/v1/options/providers/')
  }

}

export default OptionsApi
