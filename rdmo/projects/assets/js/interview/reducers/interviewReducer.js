import {
  FETCH_NAVIGATION_ERROR,
  FETCH_NAVIGATION_SUCCESS,
  FETCH_PAGE_ERROR,
  FETCH_PAGE_SUCCESS,
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
  done: null,
  page: null,
  navigation: null,
  values: null,
  attributes: [],
  sets: [],
  errors: {}
}

export default function interviewReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_PAGE_SUCCESS:
      return { ...state, page: action.page, done: action.done }
    case FETCH_NAVIGATION_SUCCESS:
      return { ...state, navigation: action.navigation }
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
      return {...state, values: state.values.filter((value) => value !== action.value)}
    case CREATE_SET:
      return { ...state, values: action.values, sets: action.sets }
    case DELETE_SET_SUCCESS:
      return {
        ...state,
        values: state.values.filter((value) => !action.values.includes(value)),
        sets: state.sets.filter((set) => !action.sets.includes(set))
      }
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
