import BaseApi from 'rdmo/core/assets/js/api/BaseApi'
import { encodeParams } from 'rdmo/core/assets/js/utils/api'
import { isNil, isUndefined } from 'lodash'

class ValueApi extends BaseApi {

  static fetchValues(projectId, params) {
    if (isNil(projectId)) {
      return this.get(`/api/v1/projects/values/?${encodeParams(params)}`)
    } else {
      return this.get(`/api/v1/projects/projects/${projectId}/values/?${encodeParams(params)}`)
    }
  }

  static storeValue(projectId, value) {
    if (isUndefined(value.id)) {
      return this.post(`/api/v1/projects/projects/${projectId}/values/`, value)
    } else {
      return this.put(`/api/v1/projects/projects/${projectId}/values/${value.id}/`, value)
    }
  }

  static storeFile(projectId, value, file) {
    const formData = new FormData()
    formData.append('file', file)

    return this.postFormData(`/api/v1/projects/projects/${projectId}/values/${value.id}/file/`, formData)
  }

  static deleteValue(projectId, value) {
    if (!isUndefined(value.id)) {
      return this.delete(`/api/v1/projects/projects/${projectId}/values/${value.id}/`)
    }
  }

  static copySet(projectId, setValue, copySetValue) {
    return this.post(`/api/v1/projects/projects/${projectId}/values/set/`, {
      ...setValue, copySetValue: copySetValue.id
    })
  }

  static deleteSet(projectId, setValue) {
    return this.delete(`/api/v1/projects/projects/${projectId}/values/${setValue.id}/set/`)
  }

}

export default ValueApi
