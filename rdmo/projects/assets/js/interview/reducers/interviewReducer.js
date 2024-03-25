import {
  FETCH_NAVIGATION_ERROR,
  FETCH_NAVIGATION_SUCCESS,
  FETCH_OVERVIEW_ERROR,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_PAGE_ERROR,
  FETCH_PAGE_SUCCESS,
  FETCH_PROGRESS_ERROR,
  FETCH_PROGRESS_SUCCESS,
} from '../actions/types'

const initialState = {
  show: false
}

export default function configReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_OVERVIEW_SUCCESS:
      return { ...state, overview: action.overview }
    case FETCH_PROGRESS_SUCCESS:
      return { ...state, progress: action.progress }
    case FETCH_NAVIGATION_SUCCESS:
      return { ...state, navigation: action.navigation, show: true }
    case FETCH_PAGE_SUCCESS:
      return { ...state, page: action.page }
    case FETCH_OVERVIEW_ERROR:
    case FETCH_PROGRESS_ERROR:
    case FETCH_NAVIGATION_ERROR:
    case FETCH_PAGE_ERROR:
      return { errors: action.errors }
    default:
      return state
  }
}
