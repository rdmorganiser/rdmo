import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  views: null,
  answers: null,
  files: null,
  current: null
}

const setCurrentView = (state, action) => {
  state.current = action.payload
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
    fetchSendIssueAnswersInit: keepState,
    fetchSendIssueAnswersSuccess(state, action) {
      state.answers = action.payload
    },
    fetchSendIssueAnswersError: keepState,
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
      state.current = null
    },
    setProjectAnswers: setCurrentView
  }
})

export const actions = documentSlice.actions

export default documentSlice.reducer
