import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  memberships: null,
  invites: null
}

const removeMembership = (state, action) => {
  state.memberships = state.memberships?.filter(m => m.id !== action.payload)
}

const membershipSlice = createSlice({
  name: 'membership',
  initialState,
  reducers: {
    fetchProjectMembershipsSuccess(state, action) {
      state.memberships = action.payload
    },
    fetchProjectInvitesSuccess(state, action) {
      state.invites = action.payload
    },
    createProjectMemberSuccess(state, action) {
      state.memberships = [...(state.memberships || []), action.payload]
    },
    updateProjectMemberSuccess(state, action) {
      state.memberships = state.memberships?.map(m => (
        m.id == action.payload.id ? { ...m, role: action.payload.role } : m
      ))
    },
    deleteProjectMemberSuccess: removeMembership,
    sendInviteSuccess(state, action) {
      state.invites.push(action.payload)
    },
    updateProjectInviteSuccess(state, action) {
      state.invites = state.invites?.map(i => (
        i.id == action.payload.id ? { ...i, role: action.payload.role } : i
      ))
    },
    deleteProjectInviteSuccess(state, action) {
      state.invites = state.invites.filter(i => i.id !== action.payload)
    },
    leaveProjectSuccess: removeMembership
  }
})

export const actions = membershipSlice.actions

export default membershipSlice.reducer
