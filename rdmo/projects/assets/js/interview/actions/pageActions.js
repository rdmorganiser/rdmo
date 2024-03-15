import PagesApi from '../api/PagesApi'
import ProjectsApi from '../api/ProjectsApi'
import ValuesApi from '../api/ValuesApi'

import { FETCH_PAGE_SUCCESS, FETCH_PAGE_ERROR, UPLOAD_FILE_SUCCESS, UPLOAD_FILE_ERROR, JUMP, PREV, NEXT } from './types'

export function fetchPage() {
  return (dispatch) => Promise.all([
    PagesApi.fetchContinue(12),
    ProjectsApi.fetchProject(12),
    ProjectsApi.fetchOverview(12),
    ProjectsApi.fetchProgress(12),
    ProjectsApi.fetchNavigation(12, 1)
  ]).then(([page, project, overview, progress, navigation]) => dispatch(fetchPageSuccess({
    page, project, overview, progress, navigation
  })))
}

export function fetchPageSuccess(page) {
  return {type: FETCH_PAGE_SUCCESS, page}
}

export function fetchPageError(errors) {
  return {type: FETCH_PAGE_ERROR, errors}
}

export function uploadFile(projectId, valueId, file) {
  return (dispatch) => ValuesApi.uploadFile(projectId, valueId, file).then((value) => {
    dispatch(uploadFileSuccess(value))
  })
}

export function uploadFileSuccess(value) {
  return {type: UPLOAD_FILE_SUCCESS, value}
}

export function uploadFileError(value) {
  return {type: UPLOAD_FILE_ERROR, value}
}

export function jump(section, page = null) {
  return {type: JUMP, section, page}
}

export function prev() {
  return {type: PREV}
}

export function next() {
  return {type: NEXT}
}
