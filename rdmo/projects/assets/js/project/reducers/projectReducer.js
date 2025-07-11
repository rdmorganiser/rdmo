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
} from '../actions/actionTypes'

const initialState = {
  project: null
}

export default function projectReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_PROJECT_SUCCESS:
      return { ...state, project: action.project }
    case FETCH_PROJECT_INIT:
      return { ...state, errors: [] }
    case FETCH_PROJECT_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    case UPDATE_PROJECT_SUCCESS:
      return { ...state, project: action.project }
    case UPDATE_PROJECT_INIT:
      return { ...state, errors: [] }
    case UPDATE_PROJECT_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case DELETE_PROJECT_SUCCESS:
      return { ...state, project: null }
    case DELETE_PROJECT_INIT:
      return { ...state, errors: [] }
    case DELETE_PROJECT_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    default:
      return state
  }
}
