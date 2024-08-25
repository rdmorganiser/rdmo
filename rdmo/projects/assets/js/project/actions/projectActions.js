import ProjectsApi from '../api/ProjectApi'

import { projectId } from '../utils/meta'

import {
  FETCH_PROJECT_INIT,
  FETCH_PROJECT_SUCCESS,
  FETCH_PROJECT_ERROR
} from './actionTypes'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'

export function fetchProject() {
  return (dispatch) => {
    dispatch(addToPending('fetchProject'))
    dispatch(fetchProjectInit())

    return ProjectsApi.fetchProject(projectId)
      .then((overview) => {
        dispatch(removeFromPending('fetchOverview'))
        dispatch(fetchProjectSuccess(overview))
      })
      .catch((error) => {
        dispatch(removeFromPending('fetchOverview'))
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
