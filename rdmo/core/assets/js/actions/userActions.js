import { actions as errorActions } from '../reducers/errorsSlice'
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
  return errorActions.clearError('currentUser')
}

export function fetchCurrentUserSuccess(currentUser) {
  return actions.fetchCurrentUserSuccess(currentUser)
}

export function fetchCurrentUserError(error) {
  return errorActions.setError({
    source: 'currentUser',
    error: { ...serializeError(error), context: gettext('Current user') }
  })
}
