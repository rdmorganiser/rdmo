import { createSlice } from '@reduxjs/toolkit'

import { locationKeys } from '../utils/location'

const initialState = {}

const locationSlice = createSlice({
  name: 'location',
  initialState,
  reducers: {
    setLocation(state, action) {
      locationKeys.forEach(key => {
        state[key] = action.payload[key] ?? null
      })
    }
  }
})

export const actions = locationSlice.actions

export default locationSlice.reducer
