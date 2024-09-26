import ProjectsApi from '../api/ProjectsApi'
import { FETCH_PROJECTS_ERROR, FETCH_PROJECTS_INIT, FETCH_PROJECTS_SUCCESS,
         FETCH_INVITATIONS_ERROR, FETCH_INVITATIONS_INIT, FETCH_INVITATIONS_SUCCESS,
         FETCH_CATALOGS_ERROR, FETCH_CATALOGS_INIT, FETCH_CATALOGS_SUCCESS,
         FETCH_FILETYPES_ERROR, FETCH_FILETYPES_INIT, FETCH_FILETYPES_SUCCESS,
         FETCH_IMPORT_URLS_ERROR, FETCH_IMPORT_URLS_INIT, FETCH_IMPORT_URLS_SUCCESS,
         UPLOAD_PROJECT_ERROR, UPLOAD_PROJECT_INIT, UPLOAD_PROJECT_SUCCESS }
         from './actionTypes'

import * as configActions from './configActions'

export function fetchProjects(pageReset = true) {
  return function(dispatch, getState) {
    if (pageReset === true) {
      dispatch(configActions.updateConfig('params.page', '1'))
    }
    const params = getState().config.params
    dispatch(fetchProjectsInit())
    const action = (dispatch) => ProjectsApi.fetchProjects(params || {})
          .then(projects => {
            dispatch(fetchProjectsSuccess(projects, !pageReset))})

    return dispatch(action)
      .catch(error => dispatch(fetchProjectsError(error)))
  }
}

export function fetchProjectsInit() {
  return {type: FETCH_PROJECTS_INIT}
}

export function fetchProjectsSuccess(projects, shouldConcatenate) {
  return {type: FETCH_PROJECTS_SUCCESS, projects, shouldConcatenate}
}

export function fetchProjectsError(error) {
  return function(dispatch) {
    if (error.constructor.name === 'BadRequestError' && error.errors.catalog) {
      dispatch(configActions.deleteConfig('params.catalog'))
      dispatch(fetchProjects())
    } else {
      dispatch({type: FETCH_PROJECTS_ERROR, error})
    }
  }
}

export function fetchCatalogs() {
  return function(dispatch) {
    dispatch(fetchCatalogsInit())
    const action = (dispatch) => ProjectsApi.fetchCatalogs().then(catalogs => {
      dispatch(fetchCatalogsSuccess(catalogs))
    })

    return dispatch(action)
      .catch(error => dispatch(fetchCatalogsError(error)))
  }
}

export function fetchCatalogsInit() {
  return {type: FETCH_CATALOGS_INIT}
}

export function fetchCatalogsSuccess(catalogs) {
  return {type: FETCH_CATALOGS_SUCCESS, catalogs}
}

export function fetchCatalogsError(error) {
  return {type: FETCH_CATALOGS_ERROR, error}
}

export function fetchAllowedFileTypes() {
  return function(dispatch) {
    dispatch(fetchAllowedFileTypesInit())
    const action = (dispatch) => ProjectsApi.fetchAllowedFileTypes().then(allowedTypes => {
      dispatch(fetchAllowedFileTypesSuccess(allowedTypes))
    })

    return dispatch(action)
      .catch(error => dispatch(fetchAllowedFileTypesError(error)))
  }
}

export function fetchAllowedFileTypesInit() {
  return {type: FETCH_FILETYPES_INIT}
}

export function fetchAllowedFileTypesSuccess(allowedTypes) {
  return {type: FETCH_FILETYPES_SUCCESS, allowedTypes}
}

export function fetchAllowedFileTypesError(error) {
  return {type: FETCH_FILETYPES_ERROR, error}
}

export function fetchImportUrls() {
  return function(dispatch) {
    dispatch(fetchImportUrlsInit())
    const action = (dispatch) => ProjectsApi.fetchDirectImportUrls().then(importUrls => {
      dispatch(fettchImportUrlsSuccess(importUrls))
    })

    return dispatch(action)
      .catch(error => dispatch(fetchImportUrlsError(error)))
  }
}

export function fetchImportUrlsInit() {
  return {type: FETCH_IMPORT_URLS_INIT}
}

export function fettchImportUrlsSuccess(importUrls) {
  return {type: FETCH_IMPORT_URLS_SUCCESS, importUrls}
}

export function fetchImportUrlsError(error) {
  return {type: FETCH_IMPORT_URLS_ERROR, error}
}

export function fetchInvitations() {
  return function(dispatch) {
    dispatch(fetchInvitationsInit())
    const action = (dispatch) => ProjectsApi.fetchInvites().then(invites => {
      dispatch(fetchInvitationsSuccess(invites))
    })

    return dispatch(action)
      .catch(error => dispatch(fetchInvitationsError(error)))
  }
}

export function fetchInvitationsInit() {
  return {type: FETCH_INVITATIONS_INIT}
}

export function fetchInvitationsSuccess(invites) {
  return {type: FETCH_INVITATIONS_SUCCESS, invites}
}

export function fetchInvitationsError(error) {
  return {type: FETCH_INVITATIONS_ERROR, error}
}

export function uploadProject(url, file) {
  return function(dispatch) {
    dispatch(uploadProjectInit())

    return ProjectsApi.uploadProject(url, file)
      .then(project => dispatch(uploadProjectSuccess(project)))
      .catch(error => {
        dispatch(uploadProjectError(error))
      })
  }
}

export function uploadProjectInit() {
  return {type: UPLOAD_PROJECT_INIT}
}

export function uploadProjectSuccess(project) {
  return {type: UPLOAD_PROJECT_SUCCESS, project}
}

export function uploadProjectError(error) {
  return {type: UPLOAD_PROJECT_ERROR, error}
}
