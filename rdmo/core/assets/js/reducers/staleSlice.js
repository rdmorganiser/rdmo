import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  items: []
}

const staleSlice = createSlice({
  name: 'stale',
  initialState,
  reducers: {
    addToStale(state, action) {
      state.items = [...new Set([...state.items, action.payload])]
    },
    removeFromStale(state, action) {
      state.items = state.items.filter(item => item !== action.payload)
    }
  }
})

export const actions = staleSlice.actions

export default staleSlice.reducer
