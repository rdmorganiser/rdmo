import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import ProjectsApi from '../api/ProjectsApi'

import {
  COPY_PROJECT_ERROR,
  COPY_PROJECT_INIT,
  COPY_PROJECT_SUCCESS,
  CREATE_PROJECT_ERROR,
  CREATE_PROJECT_INIT,
  CREATE_PROJECT_SUCCESS,
  FETCH_CATALOGS_ERROR,
  FETCH_CATALOGS_INIT,
  FETCH_CATALOGS_SUCCESS,
  FETCH_FILETYPES_ERROR,
  FETCH_FILETYPES_INIT,
  FETCH_FILETYPES_SUCCESS,
  FETCH_IMPORT_URLS_ERROR,
  FETCH_IMPORT_URLS_INIT,
  FETCH_IMPORT_URLS_SUCCESS,
  FETCH_INVITATIONS_ERROR,
  FETCH_INVITATIONS_INIT,
  FETCH_INVITATIONS_SUCCESS,
  FETCH_PROJECTS_ERROR,
  FETCH_PROJECTS_INIT,
  FETCH_PROJECTS_SUCCESS,
  UPLOAD_PROJECT_ERROR,
  UPLOAD_PROJECT_INIT,
  UPLOAD_PROJECT_SUCCESS,
} from './actionTypes'

export function fetchProjects(pageReset = true) {
  const pendingId = 'fetchProjects'

  return function (dispatch, getState) {
    if (pageReset === true) {
      dispatch(configActions.updateConfig('params.page', '1'))
    }
    const { params, myProjects } = getState().config

    dispatch(addToPending(pendingId))
    dispatch(fetchProjectsInit())

    const action = () => myProjects ? ProjectsApi.fetchUserProjects(params || {}): ProjectsApi.fetchProjects(params || {})

    return dispatch(action)
      .then(projects => dispatch(fetchProjectsSuccess(projects, !pageReset)))
      .catch(error => dispatch(fetchProjectsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchProjectsInit() {
  return { type: FETCH_PROJECTS_INIT }
}

export function fetchProjectsSuccess(projects, shouldConcatenate) {
  return { type: FETCH_PROJECTS_SUCCESS, projects, shouldConcatenate }
}

export function fetchProjectsError(error) {
  return function (dispatch) {
    if (error.constructor.name === 'BadRequestError' && error.errors.catalog) {
      dispatch(configActions.deleteConfig('params.catalog'))
      dispatch(fetchProjects())
    } else {
      dispatch({ type: FETCH_PROJECTS_ERROR, error })
    }
  }
}

export function createProject(data) {
  return function (dispatch) {
    dispatch(addToPending('createProject'))
    dispatch({ type: CREATE_PROJECT_INIT })

    return ProjectsApi.createProject(data)
      .then(project => {
        dispatch(removeFromPending('createProject'))
        dispatch({ type: CREATE_PROJECT_SUCCESS, project })

        window.location.href = `${baseUrl}/projects/${project.id}/`
      })
      .catch(error => {
        dispatch(removeFromPending('createProject'))
        dispatch({ type: CREATE_PROJECT_ERROR, error })
        throw error
      })
  }
}

export function copyProject(id, data) {
  return function (dispatch) {
    dispatch(addToPending('copyProject'))
    dispatch({ type: COPY_PROJECT_INIT })

    return ProjectsApi.copyProject(id, data)
      .then(project => {
        dispatch(removeFromPending('copyProject'))
        dispatch({ type: COPY_PROJECT_SUCCESS, project })

        window.location.href = `${baseUrl}/projects/${project.id}/`
      })
      .catch(error => {
        dispatch(removeFromPending('copyProject'))
        dispatch({ type: COPY_PROJECT_ERROR, error })
        throw error
      })
  }
}

export function refetchLoadedPages() {
  const pendingId = 'fetchProjects'

  return function (dispatch, getState) {
    const { params, myProjects } = getState().config
    const currentPage = parseInt(params?.page ?? '1', 10)
    const baseParams = { ...(params || {}) }

    const fetchPage = (nextParams) => (
      myProjects? ProjectsApi.fetchUserProjects(nextParams): ProjectsApi.fetchProjects(nextParams)
    )

    dispatch(addToPending(pendingId))

    return Promise.all(
      Array.from({ length: currentPage }, (_, index) => {
        const page = (index + 1).toString()
        return fetchPage({ ...baseParams, page })
      })
    )
      .then(responses => {
        const lastResponse = responses[responses.length - 1]

        const mergedProjects = {
          ...lastResponse,
          results: responses.flatMap(response => response.results)
        }

        return dispatch(fetchProjectsSuccess(mergedProjects, false))
      })
      .catch(error => dispatch(fetchProjectsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchCatalogs() {
  const pendingId = 'fetchCatalogs'

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(fetchCatalogsInit())

    return ProjectsApi.fetchCatalogs().then(catalogs => dispatch(fetchCatalogsSuccess(catalogs)))
      .catch(error => dispatch(fetchCatalogsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchCatalogsInit() {
  return { type: FETCH_CATALOGS_INIT }
}

export function fetchCatalogsSuccess(catalogs) {
  return { type: FETCH_CATALOGS_SUCCESS, catalogs }
}

export function fetchCatalogsError(error) {
  return { type: FETCH_CATALOGS_ERROR, error }
}

export function fetchAllowedFileTypes() {
  const pendingId = 'fetchAllowedFileTypes'

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(fetchAllowedFileTypesInit())

    const action = (dispatch) => ProjectsApi.fetchAllowedFileTypes().then(allowedTypes => {
      dispatch(fetchAllowedFileTypesSuccess(allowedTypes))
    })

    return dispatch(action)
      .catch(error => dispatch(fetchAllowedFileTypesError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchAllowedFileTypesInit() {
  return { type: FETCH_FILETYPES_INIT }
}

export function fetchAllowedFileTypesSuccess(allowedTypes) {
  return { type: FETCH_FILETYPES_SUCCESS, allowedTypes }
}

export function fetchAllowedFileTypesError(error) {
  return { type: FETCH_FILETYPES_ERROR, error }
}

export function fetchImportUrls() {
  const pendingId = 'fetchImportUrls'

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(fetchImportUrlsInit())

    const action = (dispatch) => ProjectsApi.fetchDirectImportUrls().then(importUrls => {
      dispatch(fetchImportUrlsSuccess(importUrls))
    })

    return dispatch(action)
      .catch(error => dispatch(fetchImportUrlsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchImportUrlsInit() {
  return { type: FETCH_IMPORT_URLS_INIT }
}

export function fetchImportUrlsSuccess(importUrls) {
  return { type: FETCH_IMPORT_URLS_SUCCESS, importUrls }
}

export function fetchImportUrlsError(error) {
  return { type: FETCH_IMPORT_URLS_ERROR, error }
}

export function fetchInvitations() {
  const pendingId = 'fetchInvitations'

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(fetchInvitationsInit())

    const action = (dispatch) => ProjectsApi.fetchInvites().then(invites => {
      dispatch(fetchInvitationsSuccess(invites))
    })

    return dispatch(action)
      .catch(error => dispatch(fetchInvitationsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchInvitationsInit() {
  return { type: FETCH_INVITATIONS_INIT }
}

export function fetchInvitationsSuccess(invites) {
  return { type: FETCH_INVITATIONS_SUCCESS, invites }
}

export function fetchInvitationsError(error) {
  return { type: FETCH_INVITATIONS_ERROR, error }
}

export function uploadProject(url, file) {
  const pendingId = 'uploadProject'

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(uploadProjectInit())

    return ProjectsApi.uploadProject(url, file)
      .then(project => dispatch(uploadProjectSuccess(project)))
      .catch(error => dispatch(uploadProjectError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function uploadProjectInit() {
  return { type: UPLOAD_PROJECT_INIT }
}

export function uploadProjectSuccess(project) {
  return { type: UPLOAD_PROJECT_SUCCESS, project }
}

export function uploadProjectError(error) {
  return { type: UPLOAD_PROJECT_ERROR, error }
}
