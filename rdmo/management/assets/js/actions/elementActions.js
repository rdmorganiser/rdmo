import QuestionsApi from '../api/QuestionsApi'

export function fetchCatalogsSuccess(catalogs) {
  return {type: 'elements/fetchCatalogsSuccess', catalogs}
}

export function fetchCatalogs() {
  return function(dispatch) {
    return QuestionsApi.fetchCatalogs().then(catalogs => {
      dispatch(fetchCatalogsSuccess(catalogs))
    }).catch(error => {
      throw(error)
    })
  }
}
