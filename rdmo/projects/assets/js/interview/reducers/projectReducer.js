import {
  FETCH_OVERVIEW_ERROR,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_PROGRESS_ERROR,
  FETCH_PROGRESS_SUCCESS,

} from '../actions/actionTypes'

const initialState = {
  overview: null,
  progress: null
}

export default function interviewReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_OVERVIEW_SUCCESS:
      return { ...state, overview: action.overview }
    case FETCH_PROGRESS_SUCCESS:
      return { ...state, progress: action.progress }
    case FETCH_OVERVIEW_ERROR:
    case FETCH_PROGRESS_ERROR:
      return { errors: action.errors }
    default:
      return state
  }
}
