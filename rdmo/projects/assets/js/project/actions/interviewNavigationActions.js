import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/interviewSlice'
import { actions as projectActions } from '../reducers/projectSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchNavigation() {
  const pendingId = 'fetchNavigation'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(projectActions.fetchNavigationInit())

    return ProjectApi.fetchProjectNavigation(projectId)
      .then((navigation) => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchNavigationSuccess(navigation))
      })
      .catch((error) => {
        dispatch(removeFromPending(pendingId))
        dispatch(projectActions.fetchNavigationError(serializeError(error)))
      })
  }
}

export function fetchProgress() {
  return (dispatch) => {
    dispatch(addToPending('fetchProgress'))
    dispatch(projectActions.fetchProgressInit())

    return ProjectApi.fetchProjectProgress(projectId)
      .then((progress) => {
        dispatch(removeFromPending('fetchProgress'))
        dispatch(actions.fetchProgressSuccess(progress))
      })
      .catch((error) => {
        dispatch(removeFromPending('fetchProgress'))
        dispatch(projectActions.fetchProgressError(serializeError(error)))
      })
  }
}

export function updateProgress() {
  return (dispatch) => {
    dispatch(addToPending('updateProgress'))
    dispatch(projectActions.updateProgressInit())

    return ProjectApi.updateProjectProgress(projectId)
      .then((progress) => {
        dispatch(removeFromPending('updateProgress'))
        dispatch(actions.updateProgressSuccess(progress))
      })
      .catch((error) => {
        dispatch(removeFromPending('updateProgress'))
        dispatch(projectActions.updateProgressError(serializeError(error)))
      })
  }
}
