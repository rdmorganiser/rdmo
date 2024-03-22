import Cookies from 'js-cookie'
import BaseApi from 'rdmo/core/assets/js/api/BaseApi'
import { encodeParams } from 'rdmo/core/assets/js/utils/api'
import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

class ProjectsApi extends BaseApi {

  static fetchProjects(params, fetchParams = {}) {
    return fetch('/api/v1/projects/projects/?' + encodeParams(params), fetchParams).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error(response.statusText)
      }
    })
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
                window.open(response.url, '_blank')
                // open in same window:
                // window.location.href = response.url
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
