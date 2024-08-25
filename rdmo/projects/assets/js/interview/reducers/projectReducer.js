import {
  FETCH_OVERVIEW_INIT,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_OVERVIEW_ERROR,
  FETCH_PROGRESS_INIT,
  FETCH_PROGRESS_SUCCESS,
  FETCH_PROGRESS_ERROR,
  UPDATE_PROGRESS_INIT,
  UPDATE_PROGRESS_SUCCESS,
  UPDATE_PROGRESS_ERROR,
} from '../actions/actionTypes'

const initialState = {
  overview: null,
  progress: null,
  errors: []
}

export default function interviewReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_OVERVIEW_SUCCESS:
      return { ...state, overview: action.overview }
    case FETCH_PROGRESS_SUCCESS:
    case UPDATE_PROGRESS_SUCCESS:
      return { ...state, progress: action.progress }
    case FETCH_OVERVIEW_INIT:
    case FETCH_PROGRESS_INIT:
    case UPDATE_PROGRESS_INIT:
      return { ...state, errors: [] }
    case FETCH_OVERVIEW_ERROR:
    case FETCH_PROGRESS_ERROR:
    case UPDATE_PROGRESS_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    default:
      return state
  }
}
