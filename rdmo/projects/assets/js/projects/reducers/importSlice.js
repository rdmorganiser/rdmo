import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  importKey: null,
  importList: null,
  current: null,
  uploadError: null
}

const keepState = state => state

const importSlice = createSlice({
  name: 'import',
  initialState,
  reducers: {
    setImportKey(state, action) {
      state.importKey = action.payload
    },
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
    clearUploadError(state) {
      state.uploadError = null
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
