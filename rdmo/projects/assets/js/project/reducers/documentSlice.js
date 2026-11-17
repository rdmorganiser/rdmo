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
    fetchProjectViewsInit: keepState,
    fetchProjectViewsSuccess(state, action) {
      state.views = action.payload
    },
    fetchProjectViewsError: keepState,
    fetchProjectAnswersInit: keepState,
    fetchProjectAnswersSuccess(state, action) {
      state.answers = action.payload
    },
    fetchProjectAnswersError: keepState,
    fetchAnswersInit: keepState,
    fetchAnswersSuccess: setCurrentView,
    fetchAnswersError: keepState,
    fetchViewInit: keepState,
    fetchViewSuccess: setCurrentView,
    fetchViewError: keepState,
    fetchProjectFilesInit: keepState,
    fetchProjectFilesSuccess(state, action) {
      state.files = action.payload
    },
    fetchProjectFilesError: keepState,
    downloadAnswersInit: keepState,
    downloadAnswersSuccess: keepState,
    downloadAnswersError: keepState,
    downloadViewInit: keepState,
    downloadViewSuccess: keepState,
    downloadViewError: keepState,
    clearCurrentView(state) {
      state.currentView = null
    },
    setProjectAnswers: setCurrentView
  }
})

export const actions = documentSlice.actions

export default documentSlice.reducer
