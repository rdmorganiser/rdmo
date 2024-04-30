import ProjectApi from '../api/ProjectApi'

import projectId from '../utils/projectId'

import {
  FETCH_OVERVIEW_ERROR,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_PROGRESS_ERROR,
  FETCH_PROGRESS_SUCCESS,
} from './actionTypes'

export function fetchOverview() {
  return (dispatch) => ProjectApi.fetchOverview(projectId)
    .then((overview) => dispatch(fetchOverviewSuccess(overview)))
    .catch((errors) => dispatch(fetchOverviewError(errors)))
}

export function fetchOverviewSuccess(overview) {
  return {type: FETCH_OVERVIEW_SUCCESS, overview}
}

export function fetchOverviewError(errors) {
  return {type: FETCH_OVERVIEW_ERROR, errors}
}

export function fetchProgress() {
  return (dispatch) => ProjectApi.fetchProgress(projectId)
    .then((progress) => dispatch(fetchProgressSuccess(progress)))
    .catch((errors) => dispatch(fetchProgressError(errors)))
}

export function fetchProgressSuccess(progress) {
  return {type: FETCH_PROGRESS_SUCCESS, progress}
}

export function fetchProgressError(errors) {
  return {type: FETCH_PROGRESS_ERROR, errors}
}
