import * as actionTypes from '../actions/actionTypes'

const initialState = {
  project: null,
  invites: null,
  errors: [],
  currentView: null,
}

const clearErrors = (state) => ({
  ...state,
  errors: []
})

const appendError = (state, action) => ({
  ...state,
  errors: [...state.errors, { actionType: action.type, ...action.error }]
})

export default function projectReducer(state = initialState, action) {
  switch (action.type) {
    // INIT actions - clear errors
    case actionTypes.FETCH_PROJECT_INIT:
    case actionTypes.UPDATE_PROJECT_INIT:
    case actionTypes.DELETE_PROJECT_INIT:
    case actionTypes.FETCH_PROJECT_INVITES_INIT:
    case actionTypes.CREATE_PROJECT_MEMBER_INIT:
    case actionTypes.UPDATE_PROJECT_MEMBER_INIT:
    case actionTypes.DELETE_PROJECT_MEMBER_INIT:
    case actionTypes.SEND_INVITE_INIT:
    case actionTypes.UPDATE_PROJECT_INVITE_INIT:
    case actionTypes.DELETE_PROJECT_INVITE_INIT:
    case actionTypes.LEAVE_PROJECT_INIT:
    case actionTypes.CREATE_SNAPSHOT_INIT:
    case actionTypes.UPDATE_SNAPSHOT_INIT:
    case actionTypes.DELETE_SNAPSHOT_INIT:
    case actionTypes.FETCH_ANSWERS_INIT:
    case actionTypes.FETCH_VIEW_INIT:
    case actionTypes.CLEAR_PROJECT_ERRORS:
      return clearErrors(state)
    // ERROR actions - append error
    case actionTypes.FETCH_PROJECT_ERROR:
    case actionTypes.UPDATE_PROJECT_ERROR:
    case actionTypes.DELETE_PROJECT_ERROR:
    case actionTypes.FETCH_PROJECT_INVITES_ERROR:
    case actionTypes.CREATE_PROJECT_MEMBER_ERROR:
    case actionTypes.UPDATE_PROJECT_MEMBER_ERROR:
    case actionTypes.DELETE_PROJECT_MEMBER_ERROR:
    case actionTypes.SEND_INVITE_ERROR:
    case actionTypes.UPDATE_PROJECT_INVITE_ERROR:
    case actionTypes.DELETE_PROJECT_INVITE_ERROR:
    case actionTypes.LEAVE_PROJECT_ERROR:
    case actionTypes.CREATE_SNAPSHOT_ERROR:
    case actionTypes.UPDATE_SNAPSHOT_ERROR:
    case actionTypes.DELETE_SNAPSHOT_ERROR:
    case actionTypes.FETCH_ANSWERS_ERROR:
    case actionTypes.FETCH_VIEW_ERROR:
      return appendError(state, action)
    case actionTypes.FETCH_PROJECT_SUCCESS:
      return { ...state, project: action.project }
    case actionTypes.UPDATE_PROJECT_SUCCESS:
      return { ...state, project: action.project }
    case actionTypes.DELETE_PROJECT_SUCCESS:
      return { ...state, project: null }
    case actionTypes.FETCH_PROJECT_INVITES_SUCCESS:
      return { ...state, invites: action.invites }
    case actionTypes.CREATE_PROJECT_MEMBER_SUCCESS:
      return { ...state, project: { ...state.project, memberships: [...(state.project?.memberships || []), action.member] } }
    case actionTypes.UPDATE_PROJECT_MEMBER_SUCCESS:
      return {
        ...state,
        project: {
          ...state.project,
          memberships: state.project?.memberships.map(m => (m.id == action.member.id ? { ...m, role: action.member.role } : m))
        }
      }
    case actionTypes.DELETE_PROJECT_MEMBER_SUCCESS: {
      return {
        ...state,
        project: {
          ...state.project,
          memberships: state.project.memberships?.filter(m => m.id !== action.membershipId)
        }
      }
    }
    case actionTypes.SEND_INVITE_SUCCESS:
      return { ...state, invites: [...state.invites, action.invite] }
    case actionTypes.UPDATE_PROJECT_INVITE_SUCCESS:
      return {
        ...state,
        invites: state.invites?.map(i => (i.id == action.invite.id ? { ...i, role: action.invite.role } : i))
      }
    case actionTypes.DELETE_PROJECT_INVITE_SUCCESS: {
      return { ...state, invites: state.invites.filter(i => i.id !== action.inviteId) }
    }
    case actionTypes.LEAVE_PROJECT_SUCCESS: {
      return {
        ...state,
        project: {
          ...state.project,
          memberships: state.project.memberships?.filter(m => m.id !== action.membershipId)
        }
      }
    }
    case actionTypes.CREATE_SNAPSHOT_SUCCESS:
      return {
        ...state,
        project: {
          ...state.project,
          snapshots: [...(state.project?.snapshots || []), action.snapshot]
        }
      }
    case actionTypes.DELETE_SNAPSHOT_SUCCESS: {
      return {
        ...state,
        project: {
          ...state.project,
          snapshots: state.project?.snapshots.filter(s => s.id !== action.snapshotId)
        }
      }
    }

    case actionTypes.UPDATE_SNAPSHOT_SUCCESS: {
      return {
        ...state,
        project: {
          ...state.project,
          snapshots: state.project?.snapshots.map(s =>
            s.id === action.snapshot.id
              ? { ...s, ...action.snapshot }
              : s
          )
        }
      }
    }
    case actionTypes.FETCH_ANSWERS_SUCCESS:
    case actionTypes.FETCH_VIEW_SUCCESS:
    case actionTypes.SET_PROJECT_ANSWERS:
      return {
        ...state,
        currentView: action.view
      }
    case actionTypes.CLEAR_CURRENT_VIEW:
      return {
        ...state,
        currentView: null
      }
    default:
      return state
  }
}
