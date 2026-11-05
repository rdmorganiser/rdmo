import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const combinedPermissionsSlice = createSlice({
  name: 'combinedPermissions',
  initialState,
  reducers: {
    updateCombinedPermissions(_state, action) {
      return action.payload
    }
  }
})

export const actions = combinedPermissionsSlice.actions

export default combinedPermissionsSlice.reducer
