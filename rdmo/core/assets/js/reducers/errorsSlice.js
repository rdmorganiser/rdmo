import { createSlice } from '@reduxjs/toolkit'

const errorsSlice = createSlice({
  name: 'errors',
  initialState: {},
  reducers: {
    setError(state, action) {
      const { source, error } = action.payload
      state[source] = error
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
