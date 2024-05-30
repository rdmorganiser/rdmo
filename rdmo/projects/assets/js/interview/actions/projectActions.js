import ProjectApi from '../api/ProjectApi'

import projectId from '../utils/projectId'

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

export function fetchOverview() {
  return (dispatch) => {
    dispatch(fetchOverviewInit())

    return ProjectApi.fetchOverview(projectId)
      .then((overview) => dispatch(fetchOverviewSuccess(overview)))
      .catch((error) => dispatch(fetchOverviewError(error)))
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
    dispatch(fetchProgressInit())

    return ProjectApi.fetchProgress(projectId)
    .then((progress) => dispatch(fetchProgressSuccess(progress)))
    .catch((error) => dispatch(fetchProgressError(error)))
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
    dispatch(updateProgressInit())

    return ProjectApi.updateProgress(projectId)
      .then((progress) => dispatch(updateProgressSuccess(progress)))
      .catch((error) => dispatch(updateProgressError(error)))
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
