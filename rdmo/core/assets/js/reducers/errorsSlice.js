import { createSlice } from '@reduxjs/toolkit'

const errorsSlice = createSlice({
  name: 'errors',
  initialState: {},
  reducers: {
    setError(state, action) {
      const { key, error } = action.payload
      state[key] = error
    },
    clearError(state, action) {
      delete state[action.payload]
    },
    clearErrors() {
      return {}
    }
  }
})

export const actions = errorsSlice.actions

export default errorsSlice.reducer
