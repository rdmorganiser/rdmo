import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const keepState = state => state

const templateSlice = createSlice({
  name: 'templates',
  initialState,
  reducers: {
    fetchTemplatesInit: keepState,
    fetchTemplatesSuccess(state, action) {
      return { ...state, ...action.payload }
    },
    fetchTemplatesError(state, action) {
      state.errors = action.payload
    }
  }
})

export const actions = templateSlice.actions

export default templateSlice.reducer
