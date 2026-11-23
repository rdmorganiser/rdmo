import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/progressSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchNavigation() {
  const pendingId = 'fetchNavigation'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(actions.fetchNavigationInit())

    return ProjectApi.fetchProjectNavigation(projectId)
      .then((navigation) => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchNavigationSuccess(navigation))
      })
      .catch((error) => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchNavigationError(serializeError(error)))
      })
  }
}

export function fetchProgress() {
  return (dispatch) => {
    dispatch(addToPending('fetchProgress'))
    dispatch(actions.fetchProgressInit())

    return ProjectApi.fetchProjectProgress(projectId)
      .then((progress) => {
        dispatch(removeFromPending('fetchProgress'))
        dispatch(actions.fetchProgressSuccess(progress))
      })
      .catch((error) => {
        dispatch(removeFromPending('fetchProgress'))
        dispatch(actions.fetchProgressError(serializeError(error)))
      })
  }
}

export function updateProgress() {
  return (dispatch) => {
    dispatch(addToPending('updateProgress'))
    dispatch(actions.updateProgressInit())

    return ProjectApi.updateProjectProgress(projectId)
      .then((progress) => {
        dispatch(removeFromPending('updateProgress'))
        dispatch(actions.updateProgressSuccess(progress))
      })
      .catch((error) => {
        dispatch(removeFromPending('updateProgress'))
        dispatch(actions.updateProgressError(serializeError(error)))
      })
  }
}
