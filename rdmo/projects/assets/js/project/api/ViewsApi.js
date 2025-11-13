import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ViewsApi extends BaseApi {
  static fetchViews() {
    return this.get('/api/v1/projects/views/views/')
  }
  static fetchView(viewId) {
    return this.get(`/api/v1/views/views/${viewId}/`)
  }
}

export default ViewsApi
