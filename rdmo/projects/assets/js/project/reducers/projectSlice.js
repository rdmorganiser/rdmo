import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  project: null,
  hierarchy: null,
  snapshots: null,
  views: null,
  answers: null,
  issues: null,
  memberships: null,
  catalogs: null,
  files: null,
  invites: null,
  errors: [],
  currentView: null,
  visibility: null,
  providers: null,
  integrations: []
}

const clearErrors = state => {
  state.errors = []
}

const appendError = (state, action) => {
  state.errors.push({ actionType: action.type, ...action.payload })
}

const setCurrentView = (state, action) => {
  state.currentView = action.payload
}

const setProgress = (state, action) => {
  state.progress = action.payload
}

const setVisibility = (state, action) => {
  state.visibility = action.payload
}

const removeMembership = (state, action) => {
  state.memberships = state.memberships?.filter(m => m.id !== action.payload)
}

const keepState = state => state

const projectSlice = createSlice({
  name: 'project',
  initialState,
  reducers: {
    clearProjectErrors: clearErrors,
    clearCurrentView(state) {
      state.currentView = null
    },
    setProjectAnswers: setCurrentView,

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
    fetchProjectSnapshotsSuccess(state, action) {
      state.snapshots = action.payload
    },
    fetchProjectSnapshotsError: appendError,
    fetchProjectViewsInit: clearErrors,
    fetchProjectViewsSuccess(state, action) {
      state.views = action.payload
    },
    fetchProjectViewsError: appendError,
    fetchProjectAnswersInit: clearErrors,
    fetchProjectAnswersSuccess(state, action) {
      state.answers = action.payload
    },
    fetchProjectAnswersError: appendError,
    fetchProjectMembershipsInit: clearErrors,
    fetchProjectMembershipsSuccess(state, action) {
      state.memberships = action.payload
    },
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
    fetchProjectInvitesSuccess(state, action) {
      state.invites = action.payload
    },
    fetchProjectInvitesError: appendError,
    createProjectMemberInit: clearErrors,
    createProjectMemberSuccess(state, action) {
      state.memberships = [...(state.memberships || []), action.payload]
    },
    createProjectMemberError: appendError,
    updateProjectMemberInit: clearErrors,
    updateProjectMemberSuccess(state, action) {
      const { membership, project } = action.payload
      state.memberships = state.memberships?.map(m => (
        m.id == membership.id ? { ...m, role: membership.role } : m
      ))
      state.project = project
    },
    updateProjectMemberError: appendError,
    deleteProjectMemberInit: clearErrors,
    deleteProjectMemberSuccess: removeMembership,
    deleteProjectMemberError: appendError,
    sendInviteInit: clearErrors,
    sendInviteSuccess(state, action) {
      state.invites.push(action.payload)
    },
    sendInviteError: appendError,
    updateProjectInviteInit: clearErrors,
    updateProjectInviteSuccess(state, action) {
      state.invites = state.invites?.map(i => (
        i.id == action.payload.id ? { ...i, role: action.payload.role } : i
      ))
    },
    updateProjectInviteError: appendError,
    deleteProjectInviteInit: clearErrors,
    deleteProjectInviteSuccess(state, action) {
      state.invites = state.invites.filter(i => i.id !== action.payload)
    },
    deleteProjectInviteError: appendError,
    leaveProjectInit: clearErrors,
    leaveProjectSuccess: removeMembership,
    leaveProjectError: appendError,

    createSnapshotInit: clearErrors,
    createSnapshotSuccess(state, action) {
      state.snapshots = [action.payload, ...(state.snapshots || [])]
    },
    createSnapshotError: appendError,
    updateSnapshotInit: clearErrors,
    updateSnapshotSuccess(state, action) {
      state.snapshots = state.snapshots?.map(s => (
        s.id === action.payload.id ? { ...s, ...action.payload } : s
      ))
    },
    updateSnapshotError: appendError,
    deleteSnapshotInit: clearErrors,
    deleteSnapshotSuccess(state, action) {
      state.snapshots = state.snapshots?.filter(s => s.id !== action.payload)
    },
    deleteSnapshotError: appendError,
    rollbackSnapshotSuccess(state, action) {
      return { ...state, ...action.payload }
    },

    fetchAnswersInit: clearErrors,
    fetchAnswersSuccess: setCurrentView,
    fetchAnswersError: appendError,
    fetchViewInit: clearErrors,
    fetchViewSuccess: setCurrentView,
    fetchViewError: appendError,
    fetchNavigationInit: clearErrors,
    fetchNavigationSuccess(state, action) {
      state.navigation = action.payload
    },
    fetchNavigationError: appendError,
    fetchProgressInit: clearErrors,
    fetchProgressSuccess: setProgress,
    fetchProgressError: appendError,
    updateProgressInit: clearErrors,
    updateProgressSuccess: setProgress,
    updateProgressError: appendError,

    fetchProjectFilesInit: clearErrors,
    fetchProjectFilesSuccess(state, action) {
      state.files = action.payload
    },
    fetchProjectFilesError: appendError,
    fetchProjectIssuesInit: clearErrors,
    fetchProjectIssuesSuccess(state, action) {
      state.issues = action.payload
    },
    fetchProjectIssuesError: appendError,
    sendProjectIssueEmailInit: clearErrors,
    sendProjectIssueEmailError: appendError,
    sendProjectIssueIntegrationInit: clearErrors,
    sendProjectIssueIntegrationError: appendError,

    fetchProjectVisibilityInit: clearErrors,
    fetchProjectVisibilitySuccess: setVisibility,
    fetchProjectVisibilityError: appendError,
    updateProjectVisibilitySuccess: setVisibility,
    fetchProvidersSuccess(state, action) {
      state.providers = action.payload
    },
    fetchProjectIntegrationsInit: clearErrors,
    fetchProjectIntegrationsSuccess(state, action) {
      state.integrations = action.payload
    },
    fetchProjectIntegrationsError: appendError,
    createProjectIntegrationInit: clearErrors,
    createProjectIntegrationSuccess(state, action) {
      state.integrations.push(action.payload)
    },
    createProjectIntegrationError: appendError,
    updateProjectIntegrationInit: clearErrors,
    updateProjectIntegrationSuccess(state, action) {
      state.integrations = state.integrations.map(i => (
        i.id === action.payload.id ? { ...i, ...action.payload } : i
      ))
    },
    updateProjectIntegrationError: appendError,
    deleteProjectIntegrationInit: clearErrors,
    deleteProjectIntegrationSuccess(state, action) {
      state.integrations = state.integrations.filter(i => i.id !== action.payload)
    },
    deleteProjectIntegrationError: appendError,

    updateProjectVisibilityInit: keepState,
    updateProjectVisibilityError: keepState,
    deleteProjectVisibilityInit: keepState,
    deleteProjectVisibilitySuccess: keepState,
    deleteProjectVisibilityError: keepState,
    updateProjectIssueInit: keepState,
    updateProjectIssueSuccess: keepState,
    updateProjectIssueError: keepState,
    sendProjectIssueEmailSuccess: keepState,
    sendProjectIssueIntegrationSuccess: keepState,
    rollbackSnapshotInit: keepState,
    rollbackSnapshotError: keepState,
    downloadAnswersInit: keepState,
    downloadAnswersSuccess: keepState,
    downloadAnswersError: keepState,
    downloadViewInit: keepState,
    downloadViewSuccess: keepState,
    downloadViewError: keepState
  }
})

export const actions = projectSlice.actions

export default projectSlice.reducer
