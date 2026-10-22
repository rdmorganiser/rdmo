import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  currentUser: {},
}

const setCurrentUser = (state, action) => ({ ...state, ...action.payload })

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    fetchCurrentUserInit: setCurrentUser,
    fetchCurrentUserSuccess: setCurrentUser,
    fetchCurrentUserError(state, action) {
      state.errors = action.payload.errors
    }
  }
})

export const actions = userSlice.actions

export default userSlice.reducer
