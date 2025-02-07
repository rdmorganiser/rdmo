import { FETCH_PROJECTS_ERROR, FETCH_PROJECTS_INIT, FETCH_PROJECTS_SUCCESS,
         FETCH_INVITATIONS_ERROR, FETCH_INVITATIONS_INIT, FETCH_INVITATIONS_SUCCESS,
         FETCH_CATALOGS_ERROR, FETCH_CATALOGS_INIT, FETCH_CATALOGS_SUCCESS,
         FETCH_FILETYPES_ERROR, FETCH_FILETYPES_INIT, FETCH_FILETYPES_SUCCESS,
         FETCH_IMPORT_URLS_ERROR, FETCH_IMPORT_URLS_INIT, FETCH_IMPORT_URLS_SUCCESS,
        } from '../actions/actionTypes'

const initialState = {
  ready: false,
  projects: []
}

export default function projectsReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_PROJECTS_INIT:
      return {...state, ...action.projects}
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
      return {...state, errors: action.error.errors}
    case FETCH_INVITATIONS_INIT:
      return {...state}
    case FETCH_INVITATIONS_SUCCESS:
      return {...state, invites: action.invites}
    case FETCH_INVITATIONS_ERROR:
      return {...state, errors: action.error.errors}
    case FETCH_CATALOGS_INIT:
      return {...state}
    case FETCH_CATALOGS_SUCCESS:
      return {...state, catalogs: action.catalogs}
    case FETCH_CATALOGS_ERROR:
      return {...state, errors: action.error.errors}
    case FETCH_FILETYPES_INIT:
      return {...state}
    case FETCH_FILETYPES_SUCCESS:
      return {...state, allowedTypes: action.allowedTypes}
    case FETCH_FILETYPES_ERROR:
      return {...state, errors: action.error.errors}
    case FETCH_IMPORT_URLS_INIT:
      return {...state}
    case FETCH_IMPORT_URLS_SUCCESS:
      return {...state, importUrls: action.importUrls}
    case FETCH_IMPORT_URLS_ERROR:
      return {...state, errors: action.error.errors}
    default:
       return state
  }
}
