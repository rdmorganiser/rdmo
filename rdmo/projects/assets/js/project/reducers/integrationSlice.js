import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  providers: null,
  integrations: []
}

const keepState = state => state

const integrationSlice = createSlice({
  name: 'integration',
  initialState,
  reducers: {
    fetchProvidersSuccess(state, action) {
      state.providers = action.payload
    },
    fetchProjectIntegrationsInit: keepState,
    fetchProjectIntegrationsSuccess(state, action) {
      state.integrations = action.payload
    },
    fetchProjectIntegrationsError: keepState,
    createProjectIntegrationInit: keepState,
    createProjectIntegrationSuccess(state, action) {
      state.integrations.push(action.payload)
    },
    createProjectIntegrationError: keepState,
    updateProjectIntegrationInit: keepState,
    updateProjectIntegrationSuccess(state, action) {
      state.integrations = state.integrations.map(i => (
        i.id === action.payload.id ? { ...i, ...action.payload } : i
      ))
    },
    updateProjectIntegrationError: keepState,
    deleteProjectIntegrationInit: keepState,
    deleteProjectIntegrationSuccess(state, action) {
      state.integrations = state.integrations.filter(i => i.id !== action.payload)
    },
    deleteProjectIntegrationError: keepState
  }
})

export const actions = integrationSlice.actions

export default integrationSlice.reducer
