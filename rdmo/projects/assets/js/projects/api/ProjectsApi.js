import Cookies from 'js-cookie'
import { isEmpty } from 'lodash'

import { encodeParams } from 'rdmo/core/assets/js/utils/api'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

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

  static fetchAllowedFileTypes() {
    return this.get('/api/v1/projects/imports/').then(imports => {
      const uploadImports = Object.values(imports).filter(({ upload }) => upload)

      // an upload plugin without accept allows all file types
      if (uploadImports.some(({ accept }) => isEmpty(accept))) {
        return {}
      }

      return uploadImports.reduce((allowedTypes, { accept }) => {
        Object.entries(accept).forEach(([mimeType, suffixes]) => {
          allowedTypes[mimeType] = [...new Set([...(allowedTypes[mimeType] ?? []), ...suffixes])]
        })
        return allowedTypes
      }, {})
    })
  }

  static fetchDirectImportUrls() {
    // TODO: update after import refactoring
    return this.get('/api/v1/projects/imports/').then(imports => (
      Object.entries(imports)
        .filter(([, { upload }]) => !upload)
        .map(([key, { label }]) => ({ key, label, href: '' }))
    ))
  }

  static fetchInvites() {
    return this.get('/api/v1/projects/invites/user/')
  }

  static uploadProject(url, file) {
    var formData = new FormData()
    formData.append('method', 'upload_file')
    formData.append('uploaded_file', file)
    return fetch(baseUrl + url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      body: formData
    }).catch(error => {
      throw new Error(`API error: ${error.message}`)
    }).then(response => {
      if (response.ok) {
        if (response.url) {
          // open in new window:
          // window.open(response.url, '_blank')
          // open in same window:
          window.location.href = response.url
        } else {
          throw new Error('Response does not contain a URL')
        }
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new Error(`Validation error: ${JSON.stringify(errors)}`)
        })
      } else {
        throw new Error(`API error: ${response.statusText} (${response.status})`)
      }
    })
  }

}

export default ProjectsApi
