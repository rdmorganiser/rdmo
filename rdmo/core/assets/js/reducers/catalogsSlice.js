import { createSlice } from '@reduxjs/toolkit'

const initialState = {}

const setCatalogs = (state, action) => ({ ...state, ...action.payload })

const catalogsSlice = createSlice({
  name: 'catalogs',
  initialState,
  reducers: {
    fetchCatalogsInit: setCatalogs,
    fetchCatalogsSuccess: setCatalogs,
    fetchCatalogsError(state, action) {
      state.errors = action.payload.errors
    }
  }
})

export const actions = catalogsSlice.actions

export default catalogsSlice.reducer
