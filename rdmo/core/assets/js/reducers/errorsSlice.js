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
      action.payload.forEach(key => delete state[key])
    },
    clearErrors() {
      return {}
    }
  }
})

export const actions = errorsSlice.actions

export default errorsSlice.reducer
