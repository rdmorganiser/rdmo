import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  meta: null,
  relations: [],
  additionalInputs: [],
  providers: [],
  valueTypes: [],
  widgetTypes: [],
  taskTypes: [],
  taskAreas: []
}

const constantsSlice = createSlice({
  name: 'constants',
  initialState,
  reducers: {
    fetchConstantsSuccess(state, action) {
      return { ...state, ...action.payload }
    }
  }
})

export const actions = constantsSlice.actions

export default constantsSlice.reducer
