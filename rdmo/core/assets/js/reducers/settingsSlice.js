import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    fetchSettingsSuccess(state, action) {
      return { ...state, ...action.payload }
    }
  }
})

export const actions = settingsSlice.actions

export default settingsSlice.reducer
