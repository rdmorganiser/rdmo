import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  project: null,
  hierarchy: null,
  catalogs: null,
  visibility: null
}

const setVisibility = (state, action) => {
  state.visibility = action.payload
}

const keepState = state => state

const projectSlice = createSlice({
  name: 'project',
  initialState,
  reducers: {
    fetchProjectInit: keepState,
    fetchProjectSuccess(state, action) {
      state.project = action.payload
    },
    fetchProjectError: keepState,
    fetchProjectHierarchyInit: keepState,
    fetchProjectHierarchySuccess(state, action) {
      state.hierarchy = action.payload
    },
    fetchProjectHierarchyError: keepState,
    fetchCatalogsInit: keepState,
    fetchCatalogsSuccess(state, action) {
      state.catalogs = action.payload
    },
    fetchCatalogsError: keepState,
    updateProjectInit: keepState,
    updateProjectSuccess(state, action) {
      return { ...state, ...action.payload }
    },
    updateProjectError: keepState,
    deleteProjectInit: keepState,
    deleteProjectSuccess(state) {
      state.project = null
    },
    deleteProjectError: keepState,
    fetchProjectVisibilityInit: keepState,
    fetchProjectVisibilitySuccess: setVisibility,
    fetchProjectVisibilityError: keepState,
    updateProjectVisibilitySuccess: setVisibility,
    updateProjectVisibilityInit: keepState,
    updateProjectVisibilityError: keepState,
    deleteProjectVisibilityInit: keepState,
    deleteProjectVisibilitySuccess: keepState,
    deleteProjectVisibilityError: keepState
  }
})

export const actions = projectSlice.actions

export default projectSlice.reducer
