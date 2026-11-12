import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import CatalogApi from 'rdmo/projects/assets/js/common/api/CatalogApi'

import { actions } from '../reducers/projectSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

export function fetchProject() {
  return function (dispatch) {
    dispatch(addToPending('fetchProject'))
    dispatch(actions.fetchProjectInit())

    return ProjectApi.fetchProject(projectId)
      .then(project => {
        dispatch(actions.fetchProjectSuccess(project))
        return project
      })
      .catch(error => {
        dispatch(actions.fetchProjectError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProject')))
  }
}

export function fetchProjectHierarchy() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectHierarchy'))
    dispatch(actions.fetchProjectHierarchyInit())

    return ProjectApi.fetchProjectHierarchy(projectId)
      .then(hierarchy => {
        dispatch(actions.fetchProjectHierarchySuccess(hierarchy))
        return hierarchy
      })
      .catch(error => {
        dispatch(actions.fetchProjectHierarchyError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectHierarchy')))
  }
}

export function fetchCatalogs() {
  return function (dispatch) {
    dispatch(addToPending('fetchCatalogs'))
    dispatch(actions.fetchCatalogsInit())

    return CatalogApi.fetchCatalogs()
      .then(catalogs => {
        dispatch(actions.fetchCatalogsSuccess(catalogs))
        return catalogs
      })
      .catch(error => {
        dispatch(actions.fetchCatalogsError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchCatalogs')))
  }
}

export function updateProject(data) {
  return function (dispatch, getState) {
    const state = getState()
    const id = data?.id ?? state.project?.project?.id

    if (!id) {
      console.warn('No project ID available for update.')
      return
    }

    dispatch(addToPending('updateProject'))
    dispatch(actions.updateProjectInit())

    return ProjectApi.updateProject(id, data)
      .then(() =>
        Promise.all([
          ProjectApi.fetchProject(id),
          ProjectApi.fetchProjectHierarchy(id),
        ])
      )
      .then(([project, hierarchy]) => {
        dispatch(actions.updateProjectSuccess({ project, hierarchy }))
      })
      .catch((error) => {
        dispatch(actions.updateProjectError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProject')))
  }
}

export function deleteProject(id) {
  return function (dispatch) {
    const idToDelete = id ?? projectId

    dispatch(addToPending('deleteProject'))
    dispatch(actions.deleteProjectInit())

    return ProjectApi.deleteProject(idToDelete)
      .then(() => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(actions.deleteProjectSuccess(idToDelete))

        if (!id) {
          window.location.href = `${baseUrl}/projects/`
        }
      })
      .catch((error) => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(actions.deleteProjectError(serializeError(error)))
        throw error
      })
  }
}

export function fetchProjectVisibility() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectVisibility'))
    dispatch(actions.fetchProjectVisibilityInit())

    return ProjectApi.fetchProjectVisibility(projectId)
      .then(visibility => {
        dispatch(actions.fetchProjectVisibilitySuccess(visibility))
      })
      .catch(error => {
        if (error?.status === 404) {
          dispatch(actions.fetchProjectVisibilitySuccess(null))
          return null
        }

        dispatch(actions.fetchProjectVisibilityError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectVisibility')))
  }
}

export function updateProjectVisibility(data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectVisibility'))
    dispatch(actions.updateProjectVisibilityInit())

    return ProjectApi.updateProjectVisibility(projectId, data)
      .then((visibility) => {
        dispatch(actions.updateProjectVisibilitySuccess(visibility))
      })
      .catch(error => {
        dispatch(actions.updateProjectVisibilityError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectVisibility')))
  }
}

export function deleteProjectVisibility() {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectVisibility'))
    dispatch(actions.deleteProjectVisibilityInit())

    return ProjectApi.deleteProjectVisibility(projectId)
      .then(() => {
        dispatch(fetchProjectVisibility())
        dispatch(actions.deleteProjectVisibilitySuccess())
      })
      .catch(error => {
        dispatch(actions.deleteProjectVisibilityError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('deleteProjectVisibility')))
  }
}

export function clearProjectErrors() {
  return actions.clearProjectErrors()
}
