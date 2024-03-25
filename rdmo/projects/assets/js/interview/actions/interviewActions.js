import isNil from 'lodash/isNil'

import PageApi from '../api/PageApi'
import ProjectApi from '../api/ProjectApi'

import { updateLocation } from '../utils/location'
import projectId from '../utils/projectId'

import {
  FETCH_NAVIGATION_ERROR,
  FETCH_NAVIGATION_SUCCESS,
  FETCH_OVERVIEW_ERROR,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_PAGE_ERROR,
  FETCH_PAGE_SUCCESS,
  FETCH_PROGRESS_ERROR,
  FETCH_PROGRESS_SUCCESS,
} from './types'

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

export function fetchNavigation(sectionId) {
  return (dispatch) => ProjectApi.fetchNavigation(projectId, sectionId)
    .then((navigation) => dispatch(fetchNavigationSuccess(navigation)))
    .catch((errors) => dispatch(fetchNavigationError(errors)))
}

export function fetchNavigationSuccess(navigation) {
  return {type: FETCH_NAVIGATION_SUCCESS, navigation}
}

export function fetchNavigationError(errors) {
  return {type: FETCH_NAVIGATION_ERROR, errors}
}

export function fetchPage(pageId) {
  return (dispatch) => {
    const promise = isNil(pageId) ? PageApi.fetchContinue(projectId)
                                  : PageApi.fetchPage(projectId, pageId)
    return promise.then((page) => {
      updateLocation(page.id)
      dispatch(fetchNavigation(page.section.id))
      dispatch(fetchPageSuccess(page))
    })
  }
}

export function fetchPageSuccess(page) {
  return {type: FETCH_PAGE_SUCCESS, page}
}

export function fetchPageError(errors) {
  return {type: FETCH_PAGE_ERROR, errors}
}
