import Cookies from 'js-cookie';
import isNil from 'lodash/isNil'

function ApiError(status, statusText) {
  this.status = status
  this.statusText = statusText
  this.errors = {
    'api': [`${statusText} (${status})`]
  }
}

function ValidationError(errors) {
  this.errors = errors
}

class BaseApi {

  static get(url) {
    return fetch(url).then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new ApiError(response.status, response.statusText)
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
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new ValidationError(errors)
        })
      } else {
        throw new ApiError(response.status, response.statusText)
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
    }).then(response => {
      if (response.ok) {
        return response.json()
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new ValidationError(errors)
        })
      } else {
        throw new ApiError(response.status, response.statusText)
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
    }).then(response => {
      if (response.ok) {
        return null
      } else if (response.status == 400) {
        return response.json().then(errors => {
          throw new ValidationError(errors)
        })
      } else {
        throw new ApiError(response.status, response.statusText)
      }
    })
  }

}

export default BaseApi
