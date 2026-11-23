import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  navigation: null,
  progress: null
}

const setProgress = (state, action) => {
  state.progress = action.payload
}

const keepState = state => state

const progressSlice = createSlice({
  name: 'progress',
  initialState,
  reducers: {
    fetchNavigationInit: keepState,
    fetchNavigationSuccess(state, action) {
      state.navigation = action.payload
    },
    fetchNavigationError: keepState,
    fetchProgressInit: keepState,
    fetchProgressSuccess: setProgress,
    fetchProgressError: keepState,
    updateProgressInit: keepState,
    updateProgressSuccess: setProgress,
    updateProgressError: keepState
  }
})

export const actions = progressSlice.actions

export default progressSlice.reducer
