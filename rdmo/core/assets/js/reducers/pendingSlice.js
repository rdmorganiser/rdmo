import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  items: []
}

const pendingSlice = createSlice({
  name: 'pending',
  initialState,
  reducers: {
    addToPending(state, action) {
      state.items.push(action.payload)
    },
    removeFromPending(state, action) {
      state.items = state.items.filter(item => item != action.payload)
    }
  }
})

export const actions = pendingSlice.actions

export default pendingSlice.reducer
