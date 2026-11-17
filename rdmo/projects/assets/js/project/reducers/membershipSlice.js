import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  memberships: null,
  invites: null
}

const removeMembership = (state, action) => {
  state.memberships = state.memberships?.filter(m => m.id !== action.payload)
}

const keepState = state => state

const membershipSlice = createSlice({
  name: 'membership',
  initialState,
  reducers: {
    fetchProjectMembershipsInit: keepState,
    fetchProjectMembershipsSuccess(state, action) {
      state.memberships = action.payload
    },
    fetchProjectMembershipsError: keepState,
    fetchProjectInvitesInit: keepState,
    fetchProjectInvitesSuccess(state, action) {
      state.invites = action.payload
    },
    fetchProjectInvitesError: keepState,
    createProjectMemberInit: keepState,
    createProjectMemberSuccess(state, action) {
      state.memberships = [...(state.memberships || []), action.payload]
    },
    createProjectMemberError: keepState,
    updateProjectMemberInit: keepState,
    updateProjectMemberSuccess(state, action) {
      state.memberships = state.memberships?.map(m => (
        m.id == action.payload.id ? { ...m, role: action.payload.role } : m
      ))
    },
    updateProjectMemberError: keepState,
    deleteProjectMemberInit: keepState,
    deleteProjectMemberSuccess: removeMembership,
    deleteProjectMemberError: keepState,
    sendInviteInit: keepState,
    sendInviteSuccess(state, action) {
      state.invites = [...(state.invites || []), action.payload]
    },
    sendInviteError: keepState,
    updateProjectInviteInit: keepState,
    updateProjectInviteSuccess(state, action) {
      state.invites = state.invites?.map(i => (
        i.id == action.payload.id ? { ...i, role: action.payload.role } : i
      ))
    },
    updateProjectInviteError: keepState,
    deleteProjectInviteInit: keepState,
    deleteProjectInviteSuccess(state, action) {
      state.invites = state.invites.filter(i => i.id !== action.payload)
    },
    deleteProjectInviteError: keepState,
    leaveProjectInit: keepState,
    leaveProjectSuccess: removeMembership,
    leaveProjectError: keepState
  }
})

export const actions = membershipSlice.actions

export default membershipSlice.reducer
