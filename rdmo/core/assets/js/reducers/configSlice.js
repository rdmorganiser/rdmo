import { set, unset } from 'lodash'

import { deleteConfigInLocalStorage, setConfigInLocalStorage } from '../utils/config'

import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    updateConfig(state, action) {
      const { path, value, ls } = action.payload
      if (ls) {
        setConfigInLocalStorage(state.prefix, path, value)
      }
      set(state, path, value)
    },
    deleteConfig(state, action) {
      const { path, ls } = action.payload
      if (ls) {
        deleteConfigInLocalStorage(state.prefix, path)
      }
      unset(state, path)
    }
  }
})

export const actions = configSlice.actions

export default configSlice.reducer
