import * as actionTypes from '../actions/actionTypes'

const initialState = {
  meta: null,
  relations: [],
  additionalInputs: [],
  providers: [],
  valueTypes: [],
  widgetTypes: [],
  taskTypes: [],
  taskAreas: [],
  errors: null
}

export default function constantsReducer(state = initialState, action) {
  switch (action.type) {
    case actionTypes.FETCH_CONSTANTS_INIT:
      return {...state, errors: null}
    case actionTypes.FETCH_CONSTANTS_SUCCESS:
      return {...state, ...action.constants}
    case actionTypes.FETCH_CONSTANTS_ERROR:
      return {...state, errors: action.error.errors}
    default:
      return state
  }
}
