import { createSlice } from '@reduxjs/toolkit'

import { actions as documentActions } from './documentSlice'
import { actions as integrationActions } from './integrationSlice'
import { actions as issueActions } from './issueSlice'
import { actions as membershipActions } from './membershipSlice'
import { actions as progressActions } from './progressSlice'
import { actions as projectActions } from './projectSlice'
import { actions as snapshotActions } from './snapshotSlice'

const initialState = []

const clearErrors = () => []

const appendError = (state, action) => {
  state.push({ actionType: action.type, ...action.payload })
}

const projectErrorsSlice = createSlice({
  name: 'projectErrors',
  initialState,
  reducers: {
    clearProjectErrors: clearErrors
  },
  extraReducers: builder => {
    builder.addCase(documentActions.fetchProjectViewsInit, clearErrors)
    builder.addCase(documentActions.fetchProjectViewsError, appendError)
    builder.addCase(documentActions.fetchSendIssueAnswersInit, clearErrors)
    builder.addCase(documentActions.fetchSendIssueAnswersError, appendError)
    builder.addCase(documentActions.fetchAnswersInit, clearErrors)
    builder.addCase(documentActions.fetchAnswersError, appendError)
    builder.addCase(documentActions.fetchViewInit, clearErrors)
    builder.addCase(documentActions.fetchViewError, appendError)
    builder.addCase(documentActions.fetchProjectFilesInit, clearErrors)
    builder.addCase(documentActions.fetchProjectFilesError, appendError)

    builder.addCase(integrationActions.fetchProjectIntegrationsInit, clearErrors)
    builder.addCase(integrationActions.fetchProjectIntegrationsError, appendError)
    builder.addCase(integrationActions.createProjectIntegrationInit, clearErrors)
    builder.addCase(integrationActions.createProjectIntegrationError, appendError)
    builder.addCase(integrationActions.updateProjectIntegrationInit, clearErrors)
    builder.addCase(integrationActions.updateProjectIntegrationError, appendError)
    builder.addCase(integrationActions.deleteProjectIntegrationInit, clearErrors)
    builder.addCase(integrationActions.deleteProjectIntegrationError, appendError)

    builder.addCase(issueActions.fetchProjectIssuesInit, clearErrors)
    builder.addCase(issueActions.fetchProjectIssuesError, appendError)
    builder.addCase(issueActions.sendProjectIssueEmailInit, clearErrors)
    builder.addCase(issueActions.sendProjectIssueEmailError, appendError)
    builder.addCase(issueActions.sendProjectIssueIntegrationInit, clearErrors)
    builder.addCase(issueActions.sendProjectIssueIntegrationError, appendError)

    builder.addCase(membershipActions.fetchProjectMembershipsInit, clearErrors)
    builder.addCase(membershipActions.fetchProjectMembershipsError, appendError)
    builder.addCase(membershipActions.fetchProjectInvitesInit, clearErrors)
    builder.addCase(membershipActions.fetchProjectInvitesError, appendError)
    builder.addCase(membershipActions.createProjectMemberInit, clearErrors)
    builder.addCase(membershipActions.createProjectMemberError, appendError)
    builder.addCase(membershipActions.updateProjectMemberInit, clearErrors)
    builder.addCase(membershipActions.updateProjectMemberError, appendError)
    builder.addCase(membershipActions.deleteProjectMemberInit, clearErrors)
    builder.addCase(membershipActions.deleteProjectMemberError, appendError)
    builder.addCase(membershipActions.sendInviteInit, clearErrors)
    builder.addCase(membershipActions.sendInviteError, appendError)
    builder.addCase(membershipActions.updateProjectInviteInit, clearErrors)
    builder.addCase(membershipActions.updateProjectInviteError, appendError)
    builder.addCase(membershipActions.deleteProjectInviteInit, clearErrors)
    builder.addCase(membershipActions.deleteProjectInviteError, appendError)
    builder.addCase(membershipActions.leaveProjectInit, clearErrors)
    builder.addCase(membershipActions.leaveProjectError, appendError)

    builder.addCase(progressActions.fetchNavigationInit, clearErrors)
    builder.addCase(progressActions.fetchNavigationError, appendError)
    builder.addCase(progressActions.fetchProgressInit, clearErrors)
    builder.addCase(progressActions.fetchProgressError, appendError)
    builder.addCase(progressActions.updateProgressInit, clearErrors)
    builder.addCase(progressActions.updateProgressError, appendError)

    builder.addCase(projectActions.fetchProjectInit, clearErrors)
    builder.addCase(projectActions.fetchProjectError, appendError)
    builder.addCase(projectActions.fetchProjectHierarchyInit, clearErrors)
    builder.addCase(projectActions.fetchProjectHierarchyError, appendError)
    builder.addCase(projectActions.fetchCatalogsInit, clearErrors)
    builder.addCase(projectActions.fetchCatalogsError, appendError)
    builder.addCase(projectActions.updateProjectInit, clearErrors)
    builder.addCase(projectActions.updateProjectError, appendError)
    builder.addCase(projectActions.deleteProjectInit, clearErrors)
    builder.addCase(projectActions.deleteProjectError, appendError)
    builder.addCase(projectActions.fetchProjectVisibilityInit, clearErrors)
    builder.addCase(projectActions.fetchProjectVisibilityError, appendError)

    builder.addCase(snapshotActions.fetchProjectSnapshotsInit, clearErrors)
    builder.addCase(snapshotActions.fetchProjectSnapshotsError, appendError)
    builder.addCase(snapshotActions.createSnapshotInit, clearErrors)
    builder.addCase(snapshotActions.createSnapshotError, appendError)
    builder.addCase(snapshotActions.updateSnapshotInit, clearErrors)
    builder.addCase(snapshotActions.updateSnapshotError, appendError)
    builder.addCase(snapshotActions.deleteSnapshotInit, clearErrors)
    builder.addCase(snapshotActions.deleteSnapshotError, appendError)
  }
})

export const actions = projectErrorsSlice.actions

export default projectErrorsSlice.reducer
