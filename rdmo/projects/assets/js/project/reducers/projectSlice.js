import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  project: null,
  hierarchy: null,
  catalogs: null,
  visibility: null,
  errors: []
}

const clearErrors = state => {
  state.errors = []
}

const appendError = (state, action) => {
  state.errors.push({ actionType: action.type, ...action.payload })
}

const setVisibility = (state, action) => {
  state.visibility = action.payload
}

const keepState = state => state

const projectSlice = createSlice({
  name: 'project',
  initialState,
  reducers: {
    clearProjectErrors: clearErrors,
    fetchProjectInit: clearErrors,
    fetchProjectSuccess(state, action) {
      state.project = action.payload
    },
    fetchProjectError: appendError,
    fetchProjectHierarchyInit: clearErrors,
    fetchProjectHierarchySuccess(state, action) {
      state.hierarchy = action.payload
    },
    fetchProjectHierarchyError: appendError,
    fetchProjectSnapshotsInit: clearErrors,
    fetchProjectSnapshotsError: appendError,
    fetchProjectViewsInit: clearErrors,
    fetchProjectViewsError: appendError,
    fetchProjectAnswersInit: clearErrors,
    fetchProjectAnswersError: appendError,
    fetchProjectMembershipsInit: clearErrors,
    fetchProjectMembershipsError: appendError,
    fetchCatalogsInit: clearErrors,
    fetchCatalogsSuccess(state, action) {
      state.catalogs = action.payload
    },
    fetchCatalogsError: appendError,
    updateProjectInit: clearErrors,
    updateProjectSuccess(state, action) {
      return { ...state, ...action.payload }
    },
    updateProjectError: appendError,
    deleteProjectInit: clearErrors,
    deleteProjectSuccess(state) {
      state.project = null
    },
    deleteProjectError: appendError,
    fetchProjectInvitesInit: clearErrors,
    fetchProjectInvitesError: appendError,
    createProjectMemberInit: clearErrors,
    createProjectMemberError: appendError,
    updateProjectMemberInit: clearErrors,
    updateProjectMemberError: appendError,
    deleteProjectMemberInit: clearErrors,
    deleteProjectMemberError: appendError,
    sendInviteInit: clearErrors,
    sendInviteError: appendError,
    updateProjectInviteInit: clearErrors,
    updateProjectInviteError: appendError,
    deleteProjectInviteInit: clearErrors,
    deleteProjectInviteError: appendError,
    leaveProjectInit: clearErrors,
    leaveProjectError: appendError,
    createSnapshotInit: clearErrors,
    createSnapshotError: appendError,
    updateSnapshotInit: clearErrors,
    updateSnapshotError: appendError,
    deleteSnapshotInit: clearErrors,
    deleteSnapshotError: appendError,
    fetchAnswersInit: clearErrors,
    fetchAnswersError: appendError,
    fetchViewInit: clearErrors,
    fetchViewError: appendError,
    fetchNavigationInit: clearErrors,
    fetchNavigationError: appendError,
    fetchProgressInit: clearErrors,
    fetchProgressError: appendError,
    updateProgressInit: clearErrors,
    updateProgressError: appendError,
    fetchProjectFilesInit: clearErrors,
    fetchProjectFilesError: appendError,
    fetchProjectIssuesInit: clearErrors,
    fetchProjectIssuesError: appendError,
    sendProjectIssueEmailInit: clearErrors,
    sendProjectIssueEmailError: appendError,
    sendProjectIssueIntegrationInit: clearErrors,
    sendProjectIssueIntegrationError: appendError,
    fetchProjectVisibilityInit: clearErrors,
    fetchProjectVisibilitySuccess: setVisibility,
    fetchProjectVisibilityError: appendError,
    updateProjectVisibilitySuccess: setVisibility,
    fetchProjectIntegrationsInit: clearErrors,
    fetchProjectIntegrationsError: appendError,
    createProjectIntegrationInit: clearErrors,
    createProjectIntegrationError: appendError,
    updateProjectIntegrationInit: clearErrors,
    updateProjectIntegrationError: appendError,
    deleteProjectIntegrationInit: clearErrors,
    deleteProjectIntegrationError: appendError,
    updateProjectVisibilityInit: keepState,
    updateProjectVisibilityError: keepState,
    deleteProjectVisibilityInit: keepState,
    deleteProjectVisibilitySuccess: keepState,
    deleteProjectVisibilityError: keepState,
    updateProjectIssueInit: keepState,
    updateProjectIssueError: keepState,
    rollbackSnapshotInit: keepState,
    rollbackSnapshotError: keepState,
    downloadAnswersInit: keepState,
    downloadAnswersError: keepState,
    downloadViewInit: keepState,
    downloadViewError: keepState
  }
})

export const actions = projectSlice.actions

export default projectSlice.reducer
