import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  meta: null,
  relations: [],
  additionalInputs: [],
  providers: [],
  valueTypes: [],
  widgetTypes: [],
  taskTypes: [],
  taskAreas: [],
  errors: null
}

const constantsSlice = createSlice({
  name: 'constants',
  initialState,
  reducers: {
    fetchConstantsInit(state) {
      state.errors = null
    },
    fetchConstantsSuccess(state, action) {
      return { ...state, ...action.payload }
    },
    fetchConstantsError(state, action) {
      state.errors = action.payload.errors
    }
  }
})

export const actions = constantsSlice.actions

export default constantsSlice.reducer
