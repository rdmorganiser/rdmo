import AccountsApi from '../api/AccountsApi'

import { FETCH_CURRENT_USER_ERROR, FETCH_CURRENT_USER_INIT, FETCH_CURRENT_USER_SUCCESS } from './actionTypes'

export function fetchCurrentUser() {
  return function(dispatch) {
    dispatch(fetchCurrentUserInit())

    return AccountsApi.fetchCurrentUser(true)
      .then(currentUser => dispatch(fetchCurrentUserSuccess({ currentUser })))
      .catch(error => dispatch(fetchCurrentUserError(error)))
  }
}

export function fetchCurrentUserInit() {
  return {type: FETCH_CURRENT_USER_INIT}
}

export function fetchCurrentUserSuccess(currentUser) {
  return {type: FETCH_CURRENT_USER_SUCCESS, currentUser}
}

export function fetchCurrentUserError(error) {
  return {type: FETCH_CURRENT_USER_ERROR, error}
}
