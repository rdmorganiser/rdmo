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

function getData(url) {
  return fetch(url).then(response => {
    if (response.ok) {
      return response.json()
    } else {
      throw new ApiError(response.status, response.statusText)
    }
  })
}

function postData(url, data) {
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

function putData(url, data) {
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

export { getData, postData, putData }
