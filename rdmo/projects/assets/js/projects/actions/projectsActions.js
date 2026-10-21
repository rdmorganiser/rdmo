import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import CatalogApi from 'rdmo/projects/assets/js/common/api/CatalogApi'

import { actions } from '../reducers/projectsSlice'

import ProjectsApi from '../api/ProjectsApi'

export function fetchProjects(pageReset = true) {
  const pendingId = 'fetchProjects'

  return function (dispatch, getState) {
    if (pageReset === true) {
      dispatch(configActions.updateConfig('params.page', '1'))
    }
    const { params, myProjects } = getState().config

    dispatch(addToPending(pendingId))
    dispatch(fetchProjectsInit())

    const action = () => myProjects ? (
      ProjectsApi.fetchUserProjects(params || {})
    ) : ProjectsApi.fetchProjects(params || {})

    return dispatch(action)
      .then(projects => dispatch(fetchProjectsSuccess(projects, !pageReset)))
      .catch(error => dispatch(fetchProjectsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchProjectsInit() {
  return actions.fetchProjectsInit()
}

export function fetchProjectsSuccess(projects, shouldConcatenate) {
  return actions.fetchProjectsSuccess({ projects, shouldConcatenate })
}

export function fetchProjectsError(error) {
  return function (dispatch) {
    if (error.constructor.name === 'BadRequestError' && error.errors.catalog) {
      dispatch(configActions.deleteConfig('params.catalog'))
      dispatch(fetchProjects())
    } else {
      dispatch(actions.fetchProjectsError(serializeError(error)))
    }
  }
}

export function createProject(data) {
  return function (dispatch) {
    dispatch(addToPending('createProject'))
    dispatch(actions.createProjectInit())

    return ProjectsApi.createProject(data)
      .then(project => {
        dispatch(removeFromPending('createProject'))
        dispatch(actions.createProjectSuccess(project))

        window.location.href = `${baseUrl}/projects/${project.id}/`
      })
      .catch(error => {
        dispatch(removeFromPending('createProject'))
        dispatch(actions.createProjectError(serializeError(error)))
        throw error
      })
  }
}

export function copyProject(id, data) {
  return function (dispatch) {
    dispatch(addToPending('copyProject'))
    dispatch(actions.copyProjectInit())

    return ProjectsApi.copyProject(id, data)
      .then(project => {
        dispatch(removeFromPending('copyProject'))
        dispatch(actions.copyProjectSuccess(project))

        window.location.href = `${baseUrl}/projects/${project.id}/`
      })
      .catch(error => {
        dispatch(removeFromPending('copyProject'))
        dispatch(actions.copyProjectError(serializeError(error)))
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
      myProjects ? ProjectsApi.fetchUserProjects(nextParams) : ProjectsApi.fetchProjects(nextParams)
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

    return CatalogApi.fetchCatalogs().then(catalogs => dispatch(fetchCatalogsSuccess(catalogs)))
      .catch(error => dispatch(fetchCatalogsError(error)))
      .finally(() => dispatch(removeFromPending(pendingId)))
  }
}

export function fetchCatalogsInit() {
  return actions.fetchCatalogsInit()
}

export function fetchCatalogsSuccess(catalogs) {
  return actions.fetchCatalogsSuccess(catalogs)
}

export function fetchCatalogsError(error) {
  return actions.fetchCatalogsError(serializeError(error))
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
  return actions.fetchAllowedFileTypesInit()
}

export function fetchAllowedFileTypesSuccess(allowedTypes) {
  return actions.fetchAllowedFileTypesSuccess(allowedTypes)
}

export function fetchAllowedFileTypesError(error) {
  return actions.fetchAllowedFileTypesError(serializeError(error))
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
  return actions.fetchImportUrlsInit()
}

export function fetchImportUrlsSuccess(importUrls) {
  return actions.fetchImportUrlsSuccess(importUrls)
}

export function fetchImportUrlsError(error) {
  return actions.fetchImportUrlsError(serializeError(error))
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
  return actions.fetchInvitationsInit()
}

export function fetchInvitationsSuccess(invites) {
  return actions.fetchInvitationsSuccess(invites)
}

export function fetchInvitationsError(error) {
  return actions.fetchInvitationsError(serializeError(error))
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
  return actions.uploadProjectInit()
}

export function uploadProjectSuccess(project) {
  return actions.uploadProjectSuccess(project)
}

export function uploadProjectError(error) {
  return actions.uploadProjectError(serializeError(error))
}
