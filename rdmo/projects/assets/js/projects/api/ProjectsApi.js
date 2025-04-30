import Cookies from 'js-cookie'
import BaseApi from 'rdmo/core/assets/js/api/BaseApi'
import { encodeParams } from 'rdmo/core/assets/js/utils/api'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

function BadRequestError(errors) {
  this.errors = errors
}

class ProjectsApi extends BaseApi {

  static fetchProjects(params, fetchParams = {}) {
    return fetch('/api/v1/projects/projects/?' + encodeParams(params), fetchParams).then(response => {
      if (response.ok) {
        return response.json()
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new BadRequestError(errors)
        })
      } else {
        throw new Error(response.statusText)
      }
    })
  }

  static fetchAllowedFileTypes() {
    return fetch('/api/v1/projects/projects/upload-accept/')
      .then(response => {
        if (response.ok) {
          return response.text()
            .then(text => {
              try {
                // Attempt to parse the text as JSON
                const jsonData = JSON.parse(text)
                // Check if the parsed data is an array
                if (Array.isArray(jsonData)) {
                  return jsonData
                }
              } catch (error) {
                // If JSON.parse fails, handle text as plain string below
              }

              // If it's not a JSON array, process it as a string
              const cleanedText = text.replace(/^"|"$/g, '')
              return cleanedText ? cleanedText.split(',') : []
            })
        } else {
          throw new Error(response.statusText)
        }
      })
  }

  static fetchDirectImportUrls() {
    return fetch('/api/v1/projects/projects/imports/')
      .then(response => {
        if (response.ok) {
          return response.json()
        } else {
          throw new Error(response.statusText)
        }
      })
  }

  static fetchInvites() {
    return fetch('/api/v1/projects/invites/user')
      .then(response => {
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
