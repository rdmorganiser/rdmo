import { isNil } from 'lodash'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/documentSlice'
import { actions as projectActions } from '../reducers/projectSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchProjectViews() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectViews'))
    dispatch(projectActions.fetchProjectViewsInit())

    return ProjectApi.fetchProjectViews(projectId)
      .then(views => {
        dispatch(actions.fetchProjectViewsSuccess(views))
        return views
      })
      .catch(error => {
        dispatch(projectActions.fetchProjectViewsError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectViews')))
  }
}

export function fetchProjectAnswers() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectAnswers'))
    dispatch(projectActions.fetchProjectAnswersInit())

    return ProjectApi.fetchProjectAnswers(projectId)
      .then(answers => {
        dispatch(actions.fetchProjectAnswersSuccess(answers))
        return answers
      })
      .catch(error => {
        dispatch(projectActions.fetchProjectAnswersError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectAnswers')))
  }
}

export function fetchAnswers(snapshotId, params = {}) {
  const pendingId = isNil(snapshotId) ? 'fetchAnswers' : `fetchAnswers/${snapshotId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(projectActions.fetchAnswersInit())

    return ProjectApi.fetchProjectAnswers(projectId, snapshotId, params)
      .then(view => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchAnswersSuccess(view))
        return view
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch(projectActions.fetchAnswersError(serializeError(error)))
        throw error
      })
  }
}

export function fetchView(snapshotId, viewId) {
  const pendingId = isNil(snapshotId) ? `fetchView/${viewId}` : `fetchView/${snapshotId}/${viewId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(projectActions.fetchViewInit())

    return ProjectApi.fetchProjectView(projectId, snapshotId, viewId)
      .then(view => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchViewSuccess(view))
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch(projectActions.fetchViewError(serializeError(error)))
      })
  }
}

export function fetchProjectFiles(snapshotId) {
  const pendingId = isNil(snapshotId) ? 'fetchProjectFiles' : `fetchProjectFiles/${snapshotId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(projectActions.fetchProjectFilesInit())

    return ProjectApi.fetchProjectFiles(projectId, snapshotId)
      .then(files => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchProjectFilesSuccess(files))
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch(projectActions.fetchProjectFilesError(serializeError(error)))
        throw error
      })
  }
}

export function downloadAnswers(snapshotId, format, params = {}) {
  return function (dispatch) {
    dispatch(addToPending('downloadAnswers'))
    dispatch(projectActions.downloadAnswersInit())

    return ProjectApi.downloadProjectAnswers(projectId, snapshotId, format, params)
      .then(() => dispatch(actions.downloadAnswersSuccess()))
      .catch(error => dispatch(projectActions.downloadAnswersError(serializeError(error))))
      .finally(() => dispatch(removeFromPending('downloadAnswers')))
  }
}

export function downloadView(snapshotId, viewId, format) {
  return function (dispatch) {
    dispatch(addToPending('downloadView'))
    dispatch(projectActions.downloadViewInit())

    return ProjectApi.downloadProjectView(projectId, snapshotId, viewId, format)
      .then(() => dispatch(actions.downloadViewSuccess()))
      .catch(error => dispatch(projectActions.downloadViewError(serializeError(error))))
      .finally(() => dispatch(removeFromPending('downloadView')))
  }
}

export function clearCurrentView() {
  return actions.clearCurrentView()
}

export function setProjectAnswers(view) {
  return function (dispatch) {
    dispatch(actions.setProjectAnswers(view))
  }
}
