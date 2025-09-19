import * as actionTypes from '../actions/actionTypes'

const initialState = {
  project: null,
  invites: null,
  errors: []
}

export default function projectReducer(state = initialState, action) {
  switch(action.type) {
    case actionTypes.FETCH_PROJECT_SUCCESS:
      return { ...state, project: action.project }
    case actionTypes.FETCH_PROJECT_INIT:
      return { ...state, errors: [] }
    case actionTypes.FETCH_PROJECT_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    case actionTypes.UPDATE_PROJECT_SUCCESS:
      return { ...state, project: action.project }
    case actionTypes.UPDATE_PROJECT_INIT:
      return { ...state, errors: [] }
    case actionTypes.UPDATE_PROJECT_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case actionTypes.DELETE_PROJECT_SUCCESS:
      return { ...state, project: null }
    case actionTypes.DELETE_PROJECT_INIT:
      return { ...state, errors: [] }
    case actionTypes.DELETE_PROJECT_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case actionTypes.FETCH_PROJECT_INVITES_SUCCESS:
      return { ...state, invites: action.invites }
    case actionTypes.FETCH_PROJECT_INVITES_INIT:
      return { ...state, errors: [] }
    case actionTypes.FETCH_PROJECT_INVITES_ERROR:
      return { ...state, errors: [...state.errors, { actionType: action.type, ...action.error }] }
    case actionTypes.CREATE_PROJECT_MEMBER_SUCCESS:
      return { ...state, project: { ...state.project, memberships: [ ...(state.project?.memberships || []), action.member ] } }
    case actionTypes.CREATE_PROJECT_MEMBER_INIT:
      return { ...state, errors: [] }
    case actionTypes.CREATE_PROJECT_MEMBER_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case actionTypes.UPDATE_PROJECT_MEMBER_INIT:
      return { ...state, errors: [] }
    case actionTypes.UPDATE_PROJECT_MEMBER_SUCCESS:
      return {
        ...state,
        project: {
          ...state.project,
          memberships: state.project?.memberships.map(m => (m.id == action.member.id ?  { ...m, role: action.member.role } : m))
        }
      }
    case actionTypes.UPDATE_PROJECT_MEMBER_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case actionTypes.DELETE_PROJECT_MEMBER_INIT:
      return { ...state, errors: [] }
    case actionTypes.DELETE_PROJECT_MEMBER_SUCCESS: {
      return {
        ...state,
        project: {
          ...state.project,
          memberships: state.project.memberships?.filter(m => m.id !== action.membershipId)
        }
      }
    }
    case actionTypes.DELETE_PROJECT_MEMBER_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case actionTypes.SEND_INVITE_SUCCESS:
      return { ...state, invites: [...state.invites, action.invite] }
    case actionTypes.SEND_INVITE_INIT:
      return { ...state, errors: [] }
    case actionTypes.SEND_INVITE_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case actionTypes.UPDATE_PROJECT_INVITE_INIT:
      return { ...state, errors: [] }
    case actionTypes.UPDATE_PROJECT_INVITE_SUCCESS:
      return {
        ...state,
        invites: state.invites?.map(i => (i.id == action.invite.id ? { ...i, role: action.invite.role } : i))
      }
    case actionTypes.UPDATE_PROJECT_INVITE_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case actionTypes.DELETE_PROJECT_INVITE_INIT:
      return { ...state, errors: [] }
    case actionTypes.DELETE_PROJECT_INVITE_SUCCESS: {
      return { ...state, invites: state.invites.filter(i => i.id !== action.inviteId) }
    }
    case actionTypes.DELETE_PROJECT_INVITE_ERROR:
      return {
        ...state,
        errors: [...state.errors, { actionType: action.type, ...action.error }]
      }
    case actionTypes.CLEAR_PROJECT_ERRORS:
      return { ...state, errors: [] }
    default:
      return state
  }
}
