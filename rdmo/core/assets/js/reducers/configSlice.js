import { createSlice } from '@reduxjs/toolkit'
import { set, unset } from 'lodash'

import { deleteConfigInLocalStorage, setConfigInLocalStorage } from '../utils/config'

const initialState = {}

const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    updateConfig(state, action) {
      const { path, value } = action.payload
      setConfigInLocalStorage(state.prefix, path, value)
      set(state, path, value)
    },
    deleteConfig(state, action) {
      const { path } = action.payload
      deleteConfigInLocalStorage(state.prefix, path)
      unset(state, path)
    }
  }
})

export const actions = configSlice.actions

export default configSlice.reducer
