import {
  FETCH_PROJECTS_ERROR, FETCH_PROJECTS_INIT, FETCH_PROJECTS_SUCCESS,
  FETCH_INVITATIONS_ERROR, FETCH_INVITATIONS_INIT, FETCH_INVITATIONS_SUCCESS,
  FETCH_CATALOGS_ERROR, FETCH_CATALOGS_INIT, FETCH_CATALOGS_SUCCESS,
  FETCH_FILETYPES_ERROR, FETCH_FILETYPES_INIT, FETCH_FILETYPES_SUCCESS,
  FETCH_IMPORT_URLS_ERROR, FETCH_IMPORT_URLS_INIT, FETCH_IMPORT_URLS_SUCCESS,
  CREATE_PROJECT_ERROR, CREATE_PROJECT_INIT,
  COPY_PROJECT_ERROR, COPY_PROJECT_INIT,
  UPDATE_PROJECT_ERROR, UPDATE_PROJECT_INIT
} from '../actions/actionTypes'

const initialState = {
  ready: false,
  projects: [],
  errors: [],
}

export default function projectsReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_PROJECTS_INIT:
      return { ...state, ...action.projects }
    case FETCH_PROJECTS_SUCCESS: {
      return {
        ...state,
        projects: action.shouldConcatenate ? [...state.projects, ...action.projects.results] : action.projects.results,
        ready: true,
        projectsCount: action.projects.count,
        hasNext: action.projects.next !== null
      }
    }
    case FETCH_PROJECTS_ERROR:
    case CREATE_PROJECT_ERROR:
    case COPY_PROJECT_ERROR:
    case FETCH_INVITATIONS_ERROR:
    case FETCH_CATALOGS_ERROR:
    case FETCH_FILETYPES_ERROR:
    case FETCH_IMPORT_URLS_ERROR:
    case UPDATE_PROJECT_ERROR:
      return { ...state, errors: action.error.errors }
    case FETCH_INVITATIONS_INIT:
    case FETCH_CATALOGS_INIT:
    case FETCH_FILETYPES_INIT:
    case FETCH_IMPORT_URLS_INIT:
    case CREATE_PROJECT_INIT:
    case COPY_PROJECT_INIT:
    case UPDATE_PROJECT_INIT:
      return { ...state, errors: [] }
    case FETCH_INVITATIONS_SUCCESS:
      return { ...state, invites: action.invites }
    case FETCH_CATALOGS_SUCCESS:
      return { ...state, catalogs: action.catalogs }
    case FETCH_FILETYPES_SUCCESS:
      return { ...state, allowedTypes: action.allowedTypes }
    case FETCH_IMPORT_URLS_SUCCESS:
      return { ...state, importUrls: action.importUrls }
    default:
      return state
  }
}
