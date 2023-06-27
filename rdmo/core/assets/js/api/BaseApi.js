import Cookies from 'js-cookie'
import isUndefined from 'lodash/isUndefined'

function ApiError(statusText, status) {
  this.status = status
  this.statusText = statusText
  this.errors = {
    'api': isUndefined(status) ? [statusText] : [`${statusText} (${status})`]
  }
}

function ValidationError(errors) {
  this.errors = errors
}

class BaseApi {

  static get(url) {
    return fetch(url).catch(error => {
      throw new ApiError(error.message)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new ApiError(response.statusText, response.status)
      }
    })
  }

  static post(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: JSON.stringify(data)
    }).catch(error => {
      throw new ApiError(error.message)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new ValidationError(errors)
        })
      } else {
        throw new ApiError(response.statusText, response.status)
      }
    })
  }

  static put(url, data) {
    return fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: JSON.stringify(data)
    }).catch(error => {
      throw new ApiError(error.message)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new ValidationError(errors)
        })
      } else {
        throw new ApiError(response.statusText, response.status)
      }
    })
  }

  static delete(url) {
    return fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      }
    }).catch(error => {
      throw new ApiError(error.message)
    }).then(response => {
      if (response.ok) {
        return null
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new ValidationError(errors)
        })
      } else {
        throw new ApiError(response.statusText, response.status)
      }
    })
  }

  static upload(url, file) {
    var formData = new FormData()
    formData.append('file', file)

    return fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: formData
    }).catch(error => {
      throw new ApiError(error.message)
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new ValidationError(errors)
        })
      } else {
        throw new ApiError(response.statusText, response.status)
      }
    })
  }

}

export default BaseApi
