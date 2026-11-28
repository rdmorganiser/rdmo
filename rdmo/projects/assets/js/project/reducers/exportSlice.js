import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  exportList: null,
  current: null
}

const keepState = state => state

const exportSlice = createSlice({
  name: 'export',
  initialState,
  reducers: {
    fetchExportsInit: keepState,
    fetchExportsSuccess(state, action) {
      state.exportList = action.payload
    },
    fetchExportInit(state) {
      state.current = null
    },
    fetchExportSuccess(state, action) {
      state.current = action.payload
    },
    downloadExportInit: keepState,
    downloadExportSuccess: keepState,
    submitExportInit: keepState,
    submitExportSuccess(state, action) {
      state.current = action.payload
    }
  }
})

export const actions = exportSlice.actions

export default exportSlice.reducer
