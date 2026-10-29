import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  currentUser: {},
}

const setCurrentUser = (state, action) => ({ ...state, ...action.payload })

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    fetchCurrentUserSuccess: setCurrentUser
  }
})

export const actions = userSlice.actions

export default userSlice.reducer
