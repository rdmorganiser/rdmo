import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const keepState = state => state

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    fetchSettingsInit: keepState,
    fetchSettingsSuccess(state, action) {
      return { ...state, ...action.payload }
    },
    fetchSettingsError(state, action) {
      state.errors = action.payload
    }
  }
})

export const actions = settingsSlice.actions

export default settingsSlice.reducer
