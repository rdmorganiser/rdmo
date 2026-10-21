import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  roles: [],
  errors: null,
}

const rolesSlice = createSlice({
  name: 'roles',
  initialState,
  reducers: {
    fetchRolesInit(state) {
      state.errors = null
    },
    fetchRolesSuccess(state, action) {
      state.roles = action.payload
    },
    fetchRolesError(state, action) {
      state.errors = action.payload.errors
    }
  }
})

export const actions = rolesSlice.actions

export default rolesSlice.reducer
