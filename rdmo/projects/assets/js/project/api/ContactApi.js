import { encodeParams } from 'rdmo/core/assets/js/utils/api'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ContactApi extends BaseApi {

  static fetchContact(projectId, params) {
    return this.get(`/api/v1/projects/projects/${projectId}/contact/?${encodeParams(params)}`)
  }

  static sendContact(projectId, data) {
    return this.post(`/api/v1/projects/projects/${projectId}/contact/`, data)
  }

}

export default ContactApi
