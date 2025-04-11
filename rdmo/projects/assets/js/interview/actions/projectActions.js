import ProjectApi from '../api/ProjectApi'

import { projectId } from '../utils/meta'

import {
  FETCH_OVERVIEW_INIT,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_OVERVIEW_ERROR,
  FETCH_PROGRESS_INIT,
  FETCH_PROGRESS_SUCCESS,
  FETCH_PROGRESS_ERROR,
  UPDATE_PROGRESS_INIT,
  UPDATE_PROGRESS_SUCCESS,
  UPDATE_PROGRESS_ERROR,
} from './actionTypes'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

export function fetchOverview() {
  return (dispatch) => {
    dispatch(addToPending('fetchOverview'))
    dispatch(fetchOverviewInit())

    return ProjectApi.fetchOverview(projectId)
      .then((overview) => {
        dispatch(removeFromPending('fetchOverview'))
        dispatch(fetchOverviewSuccess(overview))
      })
      .catch((error) => {
        dispatch(removeFromPending('fetchOverview'))
        dispatch(fetchOverviewError(error))
      })
  }
}

export function fetchOverviewInit() {
  return {type: FETCH_OVERVIEW_INIT}
}

export function fetchOverviewSuccess(overview) {
  return {type: FETCH_OVERVIEW_SUCCESS, overview}
}

export function fetchOverviewError(error) {
  return {type: FETCH_OVERVIEW_ERROR, error}
}

export function fetchProgress() {
  return (dispatch) => {
    dispatch(addToPending('fetchProgress'))
    dispatch(fetchProgressInit())

    return ProjectApi.fetchProgress(projectId)
    .then((progress) => {
      dispatch(removeFromPending('fetchProgress'))
      dispatch(fetchProgressSuccess(progress))
    })
    .catch((error) => {
      dispatch(removeFromPending('fetchProgress'))
      dispatch(fetchProgressError(error))
    })
  }
}

export function fetchProgressInit() {
  return {type: FETCH_PROGRESS_INIT}
}

export function fetchProgressSuccess(progress) {
  return {type: FETCH_PROGRESS_SUCCESS, progress}
}

export function fetchProgressError(error) {
  return {type: FETCH_PROGRESS_ERROR, error}
}

export function updateProgress() {
  return (dispatch) => {
    dispatch(addToPending('updateProgress'))
    dispatch(updateProgressInit())

    return ProjectApi.updateProgress(projectId)
      .then((progress) => {
        dispatch(removeFromPending('updateProgress'))
        dispatch(updateProgressSuccess(progress))
      })
      .catch((error) => {
        dispatch(removeFromPending('updateProgress'))
        dispatch(updateProgressError(error))
      })
  }
}

export function updateProgressInit() {
  return {type: UPDATE_PROGRESS_INIT}
}

export function updateProgressSuccess(progress) {
  return {type: UPDATE_PROGRESS_SUCCESS, progress}
}

export function updateProgressError(error) {
  return {type: UPDATE_PROGRESS_ERROR, error}
}
