import { encodeParams } from 'rdmo/core/assets/js/utils/api'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ProjectsApi extends BaseApi {

  static fetchProjects(params) {
    const url = '/api/v1/projects/projects/?' + encodeParams(params)
    return this.get(url)
  }

  static fetchUserProjects(params) {
    const url = '/api/v1/projects/projects/user/?' + encodeParams(params)
    return this.get(url)
  }

  static createProject(data) {
    return this.post('/api/v1/projects/projects/', data)
  }

  static copyProject(id, data) {
    return this.post(`/api/v1/projects/projects/${id}/copy/`, data)
  }

  static fetchImports() {
    return this.get('/api/v1/projects/imports/')
  }

  static uploadImport(file) {
    const formData = new FormData()
    formData.append('uploaded_file', file)
    return this.postFormData('/api/v1/projects/projects/imports/', formData)
  }

  static fetchImport(key) {
    return this.get(`/api/v1/projects/projects/imports/${key}/`)
  }

  static submitImport(key, formData) {
    return this.postFormData(`/api/v1/projects/projects/imports/${key}/`, formData)
  }

  static fetchInvites() {
    return this.get('/api/v1/projects/invites/user/')
  }

}

export default ProjectsApi
