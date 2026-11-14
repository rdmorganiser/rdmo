import { createSlice } from '@reduxjs/toolkit'
import { get, set, unset } from 'lodash'

const initialState = {}

const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    updateConfig(state, action) {
      const { path, value } = action.payload
      set(state, path, value)
    },
    deleteConfig(state, action) {
      const { path } = action.payload
      unset(state, path)
    }
  },
  selectors: {
    selectConfig: (state, path, defaultValue) => get(state, path, defaultValue)
  }
})

export const actions = configSlice.actions

export const { selectConfig } = configSlice.selectors

export default configSlice.reducer
