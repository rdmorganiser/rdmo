import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  navigation: null,
  progress: null
}

const setProgress = (state, action) => {
  state.progress = action.payload
}

const progressSlice = createSlice({
  name: 'progress',
  initialState,
  reducers: {
    fetchNavigationSuccess(state, action) {
      state.navigation = action.payload
    },
    fetchProgressSuccess: setProgress,
    updateProgressSuccess: setProgress
  }
})

export const actions = progressSlice.actions

export default progressSlice.reducer
