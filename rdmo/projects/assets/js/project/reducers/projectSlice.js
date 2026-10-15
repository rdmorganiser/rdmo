import projectReducer, { initialState } from './projectReducer'
import { createSlice } from '@reduxjs/toolkit'

const projectSlice = createSlice({
  name: 'project',
  initialState,
  reducers: {
    clearProjectErrors(state) {
      state.errors = []
    },
    clearCurrentView(state) {
      state.currentView = null
    },
    setProjectAnswers(state, action) {
      state.currentView = action.payload
    }
  },
  extraReducers: builder => {
    // Delegate remaining actions to the existing reducer.
    builder.addDefaultCase(projectReducer)
  }
})

export const actions = projectSlice.actions

export default projectSlice.reducer
