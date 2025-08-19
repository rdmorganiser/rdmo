import {
  FETCH_PROJECT_INIT,
  FETCH_PROJECT_SUCCESS,
  FETCH_PROJECT_ERROR,
  UPDATE_PROJECT_INIT,
  UPDATE_PROJECT_SUCCESS,
  UPDATE_PROJECT_ERROR,
  DELETE_PROJECT_INIT,
  DELETE_PROJECT_SUCCESS,
  DELETE_PROJECT_ERROR,
  FETCH_PROJECT_INVITES_INIT,
  FETCH_PROJECT_INVITES_SUCCESS,
  FETCH_PROJECT_INVITES_ERROR,
  ADD_PROJECT_MEMBER_INIT,
  ADD_PROJECT_MEMBER_SUCCESS,
  ADD_PROJECT_MEMBER_ERROR,
  SEND_INVITE_INIT,
  SEND_INVITE_SUCCESS,
  SEND_INVITE_ERROR
} from '../actions/actionTypes'

const initialState = {
  project: null,
  invites: null
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
    case FETCH_PROJECT_INVITES_SUCCESS:
      return { ...state, invites: action.invites }
    case FETCH_PROJECT_INVITES_INIT:
      return { ...state, errors: [] }
    case FETCH_PROJECT_INVITES_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    case ADD_PROJECT_MEMBER_SUCCESS:
      return { ...state, project: { ...state.project, memberships: [ ...(state.project?.memberships || []), action.member ] } }
    case ADD_PROJECT_MEMBER_INIT:
      return { ...state, errors: [] }
    case ADD_PROJECT_MEMBER_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case SEND_INVITE_SUCCESS:
      return { ...state, invites: [...state.invites, action.invite] }
    case SEND_INVITE_INIT:
      return { ...state, errors: [] }
    case SEND_INVITE_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    default:
      return state
  }
}
