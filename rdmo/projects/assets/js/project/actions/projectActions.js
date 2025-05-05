import ProjectApi from '../api/ProjectApi'
import CatalogsApi from '/rdmo/projects/assets/js/common/api/CatalogsApi'

import { projectId } from '../utils/meta'

import {
  FETCH_PROJECT_INIT,
  FETCH_PROJECT_SUCCESS,
  FETCH_PROJECT_ERROR,
  UPDATE_PROJECT_INIT,
  UPDATE_PROJECT_SUCCESS,
  UPDATE_PROJECT_ERROR,
  DELETE_PROJECT_INIT,
  DELETE_PROJECT_SUCCESS,
  DELETE_PROJECT_ERROR
} from './actionTypes'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

// export function fetchProject() {
//   return function(dispatch) {
//     dispatch(addToPending('fetchProject'))
//     dispatch(fetchProjectInit())

//     return Promise.all([
//       ProjectApi.fetchProject(projectId),
//       ProjectApi.fetchProjectSnapshots(projectId)

//     ])
//     .then(([project, snapshots]) => {
//       project.snapshots = snapshots
//       dispatch(removeFromPending('fetchProject'))
//       dispatch(fetchProjectSuccess(project))
//     })
//     .catch(error => {
//       dispatch(removeFromPending('fetchProject'))
//       dispatch(fetchProjectError(error))
//     })
//   }
// }

export function fetchProject() {
  return function(dispatch) {
    dispatch(addToPending('fetchProject'))
    dispatch(fetchProjectInit())

    return Promise.all([
      ProjectApi.fetchProject(projectId),
      ProjectApi.fetchProjectSnapshots(projectId),
      ProjectApi.fetchProjectTasks(projectId),
      CatalogsApi.fetchCatalogs()
    ])
    .then(([project, snapshots, tasks, catalogs]) => {
      // project.snapshots = snapshots
      // project.tasks = tasks
      const projectData = {
        project: project,
        snapshots: snapshots,
        tasks: tasks,
        catalogs: catalogs
      }

      dispatch(removeFromPending('fetchProject'))
      dispatch(fetchProjectSuccess(projectData))
    })
    .catch(error => {
      dispatch(removeFromPending('fetchProject'))
      dispatch(fetchProjectError(error))
    })
  }
}

export function fetchProjectInit() {
  return {type: FETCH_PROJECT_INIT}
}

export function fetchProjectSuccess(project) {
  return {type: FETCH_PROJECT_SUCCESS, project}
}

export function fetchProjectError(error) {
  return {type: FETCH_PROJECT_ERROR, error}
}

export function updateProject(data) {
  return function (dispatch, getState) {
    const state = getState()
    const currentBundle = state.project.project
    const id = currentBundle?.project?.id

    if (!id) {
      console.warn('No project ID available for update.')
      return
    }

    dispatch(addToPending('updateProject'))
    dispatch(updateProjectInit())

    const cleanedData = { ...data }
    if (cleanedData.parent === null) {
      delete cleanedData.parent
    }

    return ProjectApi.updateProject(id, cleanedData)
    // return ProjectApi.updateProject(id, data)
      .then((updatedProject) => {
        const updatedBundle = {
          ...currentBundle,
          project: updatedProject
        }

        dispatch(removeFromPending('updateProject'))
        dispatch(updateProjectSuccess(updatedBundle))
      })
      .catch((error) => {
        dispatch(removeFromPending('updateProject'))
        dispatch(updateProjectError(error))
      })
  }
}


export function updateProjectInit() {
  return { type: UPDATE_PROJECT_INIT }
}

export function updateProjectSuccess(project) {
  return { type: UPDATE_PROJECT_SUCCESS, project }
}

export function updateProjectError(error) {
  return { type: UPDATE_PROJECT_ERROR, error }
}

export function deleteProject(projectId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProject'))
    dispatch(deleteProjectInit())

    return ProjectApi.deleteProject(projectId)
      .then(() => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(deleteProjectSuccess(projectId))
      })
      .catch((error) => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(deleteProjectError(error))
      })
  }
}

export function deleteProjectInit() {
  return { type: DELETE_PROJECT_INIT }
}

export function deleteProjectSuccess(projectId) {
  return { type: DELETE_PROJECT_SUCCESS, projectId }
}

export function deleteProjectError(error) {
  return { type: DELETE_PROJECT_ERROR, error }
}
