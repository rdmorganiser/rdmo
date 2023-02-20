import { getData } from 'rdmo/core/assets/js/utils/api'

class OptionsApi {

  static fetchOptionsets(index=false, nested=false) {
    let url = '/api/v1/options/optionsets/'
    if (index) url += 'index/'
    if (nested) url += 'nested/'
    return getData(url)
  }

  static fetchOptions(index=false) {
    let url = '/api/v1/options/options/'
    if (index) url += 'index/'
    return getData(url)
  }
}

export default OptionsApi
