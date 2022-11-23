function ApiException(status, statusText) {
  this.status = status
  this.statusText = statusText
}

function fetchJson(url) {
  return fetch(url).then(response => {
    if (!response.ok) {
      throw new ApiException(response.status, response.statusText)
    }
    return response;
  }).then(response => {
    return response.json()
  })
}

export { fetchJson }
