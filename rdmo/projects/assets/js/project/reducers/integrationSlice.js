import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  providers: null,
  integrations: []
}

const integrationSlice = createSlice({
  name: 'integration',
  initialState,
  reducers: {
    fetchProvidersSuccess(state, action) {
      state.providers = action.payload
    },
    fetchProjectIntegrationsSuccess(state, action) {
      state.integrations = action.payload
    },
    createProjectIntegrationSuccess(state, action) {
      state.integrations.push(action.payload)
    },
    updateProjectIntegrationSuccess(state, action) {
      state.integrations = state.integrations.map(i => (
        i.id === action.payload.id ? { ...i, ...action.payload } : i
      ))
    },
    deleteProjectIntegrationSuccess(state, action) {
      state.integrations = state.integrations.filter(i => i.id !== action.payload)
    }
  }
})

export const actions = integrationSlice.actions

export default integrationSlice.reducer
