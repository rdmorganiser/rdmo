import { actions } from '../reducers/groupsSlice'
import { serializeError } from '../utils/errors'

import CoreApi from '../api/CoreApi'

export function fetchGroups() {
  return function (dispatch) {
    dispatch(actions.fetchGroupsInit())

    return CoreApi.fetchGroups()
      .then(groups => {
        dispatch(actions.fetchGroupsSuccess(groups))
      })
      .catch(error => {
        dispatch(actions.fetchGroupsError(serializeError(error)))
        throw error
      })
  }
}
