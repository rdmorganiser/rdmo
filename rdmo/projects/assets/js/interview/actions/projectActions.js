import ProjectApi from '../api/ProjectApi'

import projectId from '../utils/projectId'

import {
  FETCH_OVERVIEW_INIT,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_OVERVIEW_ERROR,
  FETCH_PROGRESS_INIT,
  FETCH_PROGRESS_SUCCESS,
  FETCH_PROGRESS_ERROR,
} from './actionTypes'

export function fetchOverview() {


  return (dispatch) => ProjectApi.fetchOverview(projectId)
    .then((overview) => dispatch(fetchOverviewSuccess(overview)))
    .catch((error) => dispatch(fetchOverviewError(error)))
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
  return (dispatch) => ProjectApi.fetchProgress(projectId)
    .then((progress) => dispatch(fetchProgressSuccess(progress)))
    .catch((error) => dispatch(fetchProgressError(error)))
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
