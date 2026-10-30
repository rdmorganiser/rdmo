import CoreApi from '../api/CoreApi'

import { FETCH_GROUPS_ERROR, FETCH_GROUPS_INIT, FETCH_GROUPS_SUCCESS } from './actionTypes'

export function fetchGroups() {
  return function (dispatch) {
    dispatch({ type: FETCH_GROUPS_INIT })

    return CoreApi.fetchGroups()
      .then(groups => {
        dispatch({ type: FETCH_GROUPS_SUCCESS, groups })
      })
      .catch(error => {
        dispatch({ type: FETCH_GROUPS_ERROR, error })
        throw error
      })
  }
}
