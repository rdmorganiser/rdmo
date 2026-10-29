import { actions as errorActions } from '../reducers/errorsSlice'
import { actions } from '../reducers/groupsSlice'
import { serializeError } from '../utils/errors'

import CoreApi from '../api/CoreApi'

export function fetchGroups() {
  return function (dispatch) {
    dispatch(errorActions.clearError('groups'))

    return CoreApi.fetchGroups()
      .then(groups => {
        dispatch(actions.fetchGroupsSuccess(groups))
      })
      .catch(error => {
        dispatch(errorActions.setError({
          source: 'groups',
          error: { ...serializeError(error), context: gettext('Groups') }
        }))
        throw error
      })
  }
}
