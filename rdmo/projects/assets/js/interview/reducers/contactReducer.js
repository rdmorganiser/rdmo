import {
  FETCH_CONTACT_INIT,
  FETCH_CONTACT_SUCCESS,
  FETCH_CONTACT_ERROR,
  SEND_CONTACT_INIT,
  SEND_CONTACT_SUCCESS,
  SEND_CONTACT_ERROR,
  CLOSE_CONTACT
} from '../actions/actionTypes'

const initialState = {
  showModal: false,
  values: {},
  errors: []
}

export default function interviewReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_CONTACT_INIT:
    case SEND_CONTACT_INIT:
      return { ...state, errors: [] }
    case FETCH_CONTACT_ERROR:
    case SEND_CONTACT_ERROR:
      return { ...state, errors: action.error.errors }
    case FETCH_CONTACT_SUCCESS:
      return { ...state, showModal: true, values: action.values }
    case SEND_CONTACT_SUCCESS:
    case CLOSE_CONTACT:
      return { ...state, showModal: false, values: {} }
    default:
      return state
  }
}
