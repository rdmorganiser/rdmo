import { createSlice } from '@reduxjs/toolkit'

const initialState = []

const sitesSlice = createSlice({
  name: 'sites',
  initialState,
  reducers: {
    fetchSitesSuccess(state, action) {
      return action.payload
    }
  }
})

export const actions = sitesSlice.actions

export default sitesSlice.reducer
