import CoreApi from '../api/CoreApi'

import { FETCH_SITES_ERROR, FETCH_SITES_INIT, FETCH_SITES_SUCCESS } from './actionTypes'

export function fetchSites() {
  return function (dispatch) {
    dispatch({ type: FETCH_SITES_INIT })

    return CoreApi.fetchSites()
      .then(sites => {
        dispatch({ type: FETCH_SITES_SUCCESS, sites })
      })
      .catch(error => {
        dispatch({ type: FETCH_SITES_ERROR, error })
        throw error
      })
  }
}
