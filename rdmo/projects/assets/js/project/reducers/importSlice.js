import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  importList: null,
  current: null,
  uploadError: null
}

const keepState = state => state

const importSlice = createSlice({
  name: 'import',
  initialState,
  reducers: {
    fetchImportsInit: keepState,
    fetchImportsSuccess(state, action) {
      state.importList = action.payload
    },
    uploadImportInit(state) {
      state.uploadError = null
    },
    uploadImportSuccess: keepState,
    uploadImportError(state, action) {
      state.uploadError = action.payload
    },
    fetchImportInit(state) {
      state.current = null
    },
    fetchImportSuccess(state, action) {
      state.current = action.payload
    },
    submitImportInit: keepState,
    submitImportSuccess(state, action) {
      state.current = action.payload
    }
  }
})

export const actions = importSlice.actions

export default importSlice.reducer
