import { createSlice } from '@reduxjs/toolkit'
import { set, unset } from 'lodash'

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
  }
})

export const actions = configSlice.actions

export default configSlice.reducer
