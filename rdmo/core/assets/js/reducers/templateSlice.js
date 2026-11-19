import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const templateSlice = createSlice({
  name: 'templates',
  initialState,
  reducers: {
    fetchTemplatesSuccess(state, action) {
      return { ...state, ...action.payload }
    }
  }
})

export const actions = templateSlice.actions

export default templateSlice.reducer
