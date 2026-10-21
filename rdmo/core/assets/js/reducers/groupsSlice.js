import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const keepState = state => state

const groupsSlice = createSlice({
  name: 'groups',
  initialState,
  reducers: {
    fetchGroupsInit: keepState,
    fetchGroupsSuccess(state, action) {
      return { ...state, ...action.payload }
    },
    fetchGroupsError(state, action) {
      state.errors = action.payload
    }
  }
})

export const actions = groupsSlice.actions

export default groupsSlice.reducer
