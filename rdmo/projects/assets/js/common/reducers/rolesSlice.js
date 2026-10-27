import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  roles: [],
}

const rolesSlice = createSlice({
  name: 'roles',
  initialState,
  reducers: {
    fetchRolesSuccess(state, action) {
      state.roles = action.payload
    }
  }
})

export const actions = rolesSlice.actions

export default rolesSlice.reducer
