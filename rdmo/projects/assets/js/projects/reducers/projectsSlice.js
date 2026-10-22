import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  ready: false,
  projects: [],
  errors: [],
}

const clearErrors = state => {
  state.errors = []
}

const setErrors = (state, action) => {
  state.errors = action.payload.errors
}

const keepState = state => state

const projectsSlice = createSlice({
  name: 'projects',
  initialState,
  reducers: {
    fetchProjectsInit(state, action) {
      return { ...state, ...action.payload }
    },
    fetchProjectsSuccess(state, action) {
      const { projects, shouldConcatenate } = action.payload
      state.projects = shouldConcatenate ? [...state.projects, ...projects.results] : projects.results
      state.ready = true
      state.projectsCount = projects.count
      state.hasNext = projects.next !== null
    },
    fetchProjectsError: setErrors,
    fetchInvitationsInit: clearErrors,
    fetchInvitationsSuccess(state, action) {
      state.invites = action.payload
    },
    fetchInvitationsError: setErrors,
    fetchCatalogsInit: clearErrors,
    fetchCatalogsSuccess(state, action) {
      state.catalogs = action.payload
    },
    fetchCatalogsError: setErrors,
    fetchAllowedFileTypesInit: clearErrors,
    fetchAllowedFileTypesSuccess(state, action) {
      state.allowedTypes = action.payload
    },
    fetchAllowedFileTypesError: setErrors,
    fetchImportUrlsInit: clearErrors,
    fetchImportUrlsSuccess(state, action) {
      state.importUrls = action.payload
    },
    fetchImportUrlsError: setErrors,
    createProjectInit: clearErrors,
    createProjectSuccess: keepState,
    createProjectError: setErrors,
    copyProjectInit: clearErrors,
    copyProjectSuccess: keepState,
    copyProjectError: setErrors,
    uploadProjectInit: keepState,
    uploadProjectSuccess: keepState,
    uploadProjectError: keepState
  }
})

export const actions = projectsSlice.actions

export default projectsSlice.reducer
