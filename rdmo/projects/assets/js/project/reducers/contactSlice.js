import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  showModal: false,
  values: {},
  errors: []
}

const clearErrors = state => {
  state.errors = []
}

const setErrors = (state, action) => {
  state.errors = action.payload.errors
}

const closeContact = state => {
  state.showModal = false
  state.values = {}
}

const contactSlice = createSlice({
  name: 'contact',
  initialState,
  reducers: {
    fetchContactInit: clearErrors,
    fetchContactSuccess(state, action) {
      state.showModal = true
      state.values = action.payload
    },
    fetchContactError: setErrors,
    sendContactInit: clearErrors,
    sendContactSuccess: closeContact,
    sendContactError: setErrors,
    closeContact
  }
})

export const actions = contactSlice.actions

export default contactSlice.reducer
