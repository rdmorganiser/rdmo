import QuestionsApi from '../api/QuestionsApi'

export function fetchCatalogSuccess(catalog) {
    return {type: 'questions/fetchCatalogSuccess', catalog}
}

export function fetchCatalog(id) {
  return function(dispatch) {
    return QuestionsApi.fetchCatalog(id, true).then(catalog => {
      dispatch(fetchCatalogSuccess(catalog))
    }).catch(error => {
      throw(error)
    })
  }
}
