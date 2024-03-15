import Cookies from 'js-cookie'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

class ValuesApi extends BaseApi {

  static uploadFile(projectId, valueId, file) {
    const url = `/api/v1/projects/projects/${projectId}/values/${valueId}/file/`

    var formData = new FormData()
    formData.append('method', 'upload_file')
    formData.append('file', file)

    return fetch(baseUrl + url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        body: formData
    }).catch(error => {
        throw new Error(`API error: ${error.message}`)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else if (response.status == 400) {
        // return response.json().then(errors => {
        //   throw new ValidationError(errors)
        // })
      } else {
        // throw new ApiError(response.statusText, response.status)
      }
    })
  }

}

export default ValuesApi
