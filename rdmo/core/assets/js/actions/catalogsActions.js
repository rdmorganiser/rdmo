import CatalogsApi from '../api/CatalogsApi'
import { FETCH_CATALOGS_ERROR, FETCH_CATALOGS_INIT, FETCH_CATALOGS_SUCCESS } from './actionTypes'

export function fetchCatalogs() {
  return function(dispatch) {
    dispatch(fetchCatalogsInit())
    const action = (dispatch) => CatalogsApi.fetchCatalogs()
          .then(catalogs => {
            dispatch(fetchCatalogsSuccess({ catalogs }))})

    return dispatch(action)
      .catch(error => dispatch(fetchCatalogsError(error)))
  }
}

export function fetchCatalogsInit() {
  return {type: FETCH_CATALOGS_INIT}
}

export function fetchCatalogsSuccess(catalogs) {
  return {type: FETCH_CATALOGS_SUCCESS, catalogs}
}

export function fetchCatalogsError(error) {
  return {type: FETCH_CATALOGS_ERROR, error}
}
