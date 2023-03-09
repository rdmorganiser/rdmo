import isNil from 'lodash/isNil'

import { getData, postData, putData } from 'rdmo/core/assets/js/utils/api'

class ViewsApi {

  static fetchViews(action) {
    let url = '/api/v1/views/views/'
    if (action == 'index') url += 'index/'
    return getData(url)
  }

  static fetchView(id) {
    return getData(`/api/v1/views/views/${id}/`)
  }

  static storeView(view) {
    if (isNil(view.id)) {
      return postData(`/api/v1/views/views/`, view)
    } else {
      return putData(`/api/v1/views/views/${view.id}/`, view)
    }
  }

}

export default ViewsApi
