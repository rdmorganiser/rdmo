class QuestionsApi {

  static fetchCatalogs(index=false) {
    let url = `/api/v1/questions/catalogs/`
    if (index) {
      url += 'index/'
    }

    return fetch(url).then(response => {
      return response.json()
    }).catch(error => {
      return error
    });
  }

  static fetchCatalog(id, nested=false) {
    let url = `/api/v1/questions/catalogs/${id}/`
    if (nested) {
      url += 'nested/'
    }

    return fetch(url).then(response => {
      return response.json()
    }).catch(error => {
      return error
    });
  }

}

export default QuestionsApi
