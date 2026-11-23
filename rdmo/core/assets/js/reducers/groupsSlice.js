import { createSlice } from '@reduxjs/toolkit'

const initialState = []

const groupsSlice = createSlice({
  name: 'groups',
  initialState,
  reducers: {
    fetchGroupsSuccess(state, action) {
      return action.payload
    }
  }
})

export const actions = groupsSlice.actions

export default groupsSlice.reducer
