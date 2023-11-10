import { FETCH_PROJECTS_ERROR, FETCH_PROJECTS_INIT, FETCH_PROJECTS_SUCCESS } from '../actions/types'

const initialState = {
  projects: [],
}

export default function projectsReducer(state = initialState, action) {
  switch(action.type) {
    // fetch elements
    case FETCH_PROJECTS_INIT:
      return {...state, ...action.projects}
    case FETCH_PROJECTS_SUCCESS:
      return {...state, ...action.projects}
    case FETCH_PROJECTS_ERROR:
      return {...state, errors: action.error.errors}
    default:
       return state
  }
}
