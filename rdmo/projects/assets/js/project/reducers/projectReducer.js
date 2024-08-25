import {
  FETCH_PROJECT_INIT,
  FETCH_PROJECT_SUCCESS,
  FETCH_PROJECT_ERROR
} from '../actions/actionTypes'

const initialState = {
  project: null
}

export default function interviewReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_PROJECT_SUCCESS:
      return { ...state, project: action.project }
    case FETCH_PROJECT_INIT:
      return { ...state, errors: [] }
    case FETCH_PROJECT_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    default:
      return state
  }
}
