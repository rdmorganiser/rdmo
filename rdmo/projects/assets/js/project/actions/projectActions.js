import ProjectApi from '../api/ProjectApi'
import CatalogsApi from '/rdmo/projects/assets/js/common/api/CatalogsApi'

import { projectId } from '../utils/meta'

import {
  FETCH_PROJECT_INIT,
  FETCH_PROJECT_SUCCESS,
  FETCH_PROJECT_ERROR
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
