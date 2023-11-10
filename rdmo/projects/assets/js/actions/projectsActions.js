
import ProjectsApi from '../api/ProjectsApi'
import { FETCH_PROJECTS_ERROR, FETCH_PROJECTS_INIT, FETCH_PROJECTS_SUCCESS } from './types'

export function fetchAllProjects() {
  return function(dispatch) {
    dispatch(fetchProjectsInit())
    const action = (dispatch) => ProjectsApi.fetchProjects(true)
          .then(projects => {
            dispatch(fetchProjectsSuccess({ projects }))})

    return dispatch(action)
      .catch(error => dispatch(fetchProjectsError(error)))
  }
}

export function fetchProjectsInit() {
  return {type: FETCH_PROJECTS_INIT}
}

export function fetchProjectsSuccess(projects) {
  return {type: FETCH_PROJECTS_SUCCESS, projects}
}

export function fetchProjectsError(error) {
  return {type: FETCH_PROJECTS_ERROR, error}
}
