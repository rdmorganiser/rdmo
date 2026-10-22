import { actions } from '../reducers/userSlice'
import { serializeError } from '../utils/errors'

import AccountsApi from '../api/AccountsApi'

export function fetchCurrentUser() {
  return function(dispatch) {
    dispatch(fetchCurrentUserInit())

    return AccountsApi.fetchCurrentUser(true)
      .then(currentUser => dispatch(fetchCurrentUserSuccess({ currentUser })))
      .catch(error => dispatch(fetchCurrentUserError(error)))
  }
}

export function fetchCurrentUserInit() {
  return actions.fetchCurrentUserInit()
}

export function fetchCurrentUserSuccess(currentUser) {
  return actions.fetchCurrentUserSuccess(currentUser)
}

export function fetchCurrentUserError(error) {
  return actions.fetchCurrentUserError(serializeError(error))
}
