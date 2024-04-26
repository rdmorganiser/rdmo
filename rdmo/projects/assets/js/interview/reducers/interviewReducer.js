import {
  FETCH_NAVIGATION_ERROR,
  FETCH_NAVIGATION_SUCCESS,
  FETCH_OVERVIEW_ERROR,
  FETCH_OVERVIEW_SUCCESS,
  FETCH_PAGE_ERROR,
  FETCH_PAGE_SUCCESS,
  FETCH_PROGRESS_ERROR,
  FETCH_PROGRESS_SUCCESS,
  FETCH_VALUES_SUCCESS,
  FETCH_VALUES_ERROR,
  CREATE_VALUE,
  STORE_VALUE_SUCCESS,
  STORE_VALUE_ERROR,
  DELETE_VALUE_SUCCESS,
  DELETE_VALUE_ERROR,
  CREATE_SET,
  DELETE_SET_SUCCESS,
  DELETE_SET_ERROR
} from '../actions/actionTypes'

const initialState = {
  show: false,
  values: [],
  sets: []
}

export default function interviewReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_OVERVIEW_SUCCESS:
      return { ...state, overview: action.overview }
    case FETCH_PROGRESS_SUCCESS:
      return { ...state, progress: action.progress }
    case FETCH_NAVIGATION_SUCCESS:
      return { ...state, navigation: action.navigation }
    case FETCH_PAGE_SUCCESS:
      return { ...state, page: action.page, attributes: action.attributes }
    case FETCH_VALUES_SUCCESS:
      return { ...state, values: action.values, sets: action.sets }
    case CREATE_VALUE:
      return { ...state, values: [...state.values, action.value] }
    case STORE_VALUE_SUCCESS:
      if (action.valueIndex > -1) {
        return { ...state, values: state.values.map(
          (value, valueIndex) => valueIndex == action.valueIndex ? action.value : value
        )}
      } else {
        return { ...state, values: [...state.values, action.value] }
      }
    case DELETE_VALUE_SUCCESS:
      return { ...state, values: state.values.filter((value, valueIndex) => valueIndex != action.valueIndex)}
    case CREATE_SET:
      return { ...state, sets: [...state.sets, action.set] }
    case DELETE_SET_SUCCESS:
      return { ...state, sets: state.sets.filter((set) => set != action.set) }
    case FETCH_OVERVIEW_ERROR:
    case FETCH_PROGRESS_ERROR:
    case FETCH_NAVIGATION_ERROR:
    case FETCH_PAGE_ERROR:
    case FETCH_VALUES_ERROR:
    case STORE_VALUE_ERROR:
    case DELETE_VALUE_ERROR:
    case DELETE_SET_ERROR:
      return { errors: action.errors }
    default:
      return state
  }
}
