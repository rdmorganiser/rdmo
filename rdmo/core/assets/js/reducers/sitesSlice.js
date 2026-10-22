import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const keepState = state => state

const sitesSlice = createSlice({
  name: 'sites',
  initialState,
  reducers: {
    fetchSitesInit: keepState,
    fetchSitesSuccess(state, action) {
      return { ...state, ...action.payload }
    },
    fetchSitesError(state, action) {
      state.errors = action.payload
    }
  }
})

export const actions = sitesSlice.actions

export default sitesSlice.reducer
