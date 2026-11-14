import { actions } from '../reducers/groupsSlice'

import CoreApi from '../api/CoreApi'

import * as errorActions from './errorsActions'

export function fetchGroups() {
  return function (dispatch) {
    dispatch(errorActions.clearError('groups'))

    return CoreApi.fetchGroups()
      .then(groups => {
        dispatch(actions.fetchGroupsSuccess(groups))
      })
      .catch(error => {
        dispatch(errorActions.setError('groups', error, gettext('Groups')))
        throw error
      })
  }
}
