import isNil from 'lodash/isNil'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ViewsApi extends BaseApi {

  static fetchViews(action) {
    let url = '/api/v1/views/views/'
    if (action == 'index') url += 'index/'
    return this.get(url)
  }

  static fetchView(id) {
    return this.get(`/api/v1/views/views/${id}/`)
  }

  static storeView(view, action) {
    if (isNil(view.id)) {
      return this.post('/api/v1/views/views/', view)
    } else {
      let url= `/api/v1/views/views/${view.id}/`
      if (['add-site', 'remove-site'].includes(action)) {
        url = `/api/v1/views/view-toggle-site/${view.id}/${action}/`
      }
      return this.put(url, view)
    }
  }

  static deleteView(view) {
    return this.delete(`/api/v1/views/views/${view.id}/`)
  }

}

export default ViewsApi
