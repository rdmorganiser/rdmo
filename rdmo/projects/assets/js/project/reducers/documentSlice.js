import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  views: null,
  answers: null,
  files: null,
  currentView: null
}

const setCurrentView = (state, action) => {
  state.currentView = action.payload
}

const keepState = state => state

const documentSlice = createSlice({
  name: 'document',
  initialState,
  reducers: {
    fetchProjectViewsSuccess(state, action) {
      state.views = action.payload
    },
    fetchProjectAnswersSuccess(state, action) {
      state.answers = action.payload
    },
    fetchAnswersSuccess: setCurrentView,
    fetchViewSuccess: setCurrentView,
    fetchProjectFilesSuccess(state, action) {
      state.files = action.payload
    },
    downloadAnswersSuccess: keepState,
    downloadViewSuccess: keepState,
    clearCurrentView(state) {
      state.currentView = null
    },
    setProjectAnswers: setCurrentView
  }
})

export const actions = documentSlice.actions

export default documentSlice.reducer
