import { actions } from '../reducers/userSlice'

import AccountsApi from '../api/AccountsApi'

import * as errorActions from './errorsActions'

export function fetchCurrentUser() {
  return function(dispatch) {
    dispatch(fetchCurrentUserInit())

    return AccountsApi.fetchCurrentUser(true)
      .then(currentUser => dispatch(fetchCurrentUserSuccess({ currentUser })))
      .catch(error => dispatch(fetchCurrentUserError(error)))
  }
}

export function fetchCurrentUserInit() {
  return errorActions.clearError('currentUser')
}

export function fetchCurrentUserSuccess(currentUser) {
  return actions.fetchCurrentUserSuccess(currentUser)
}

export function fetchCurrentUserError(error) {
  return errorActions.setError('currentUser', error, gettext('Current user'))
}
