import { isNil } from 'lodash'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { addToStale } from 'rdmo/core/assets/js/actions/staleActions'
import { serializeError } from 'rdmo/core/assets/js/utils/errors'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import CatalogApi from 'rdmo/projects/assets/js/common/api/CatalogApi'

import { actions } from '../reducers/projectSlice'
import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

// asynchronous actions

// project

export function fetchProject() {

  return function (dispatch) {
    dispatch(addToPending('fetchProject'))
    dispatch(actions.fetchProjectInit())

    return Promise.all([
      ProjectApi.fetchProject(projectId),
      ProjectApi.fetchProjectHierarchy(projectId),
      ProjectApi.fetchProjectSnapshots(projectId),
      ProjectApi.fetchProjectViews(projectId),
      ProjectApi.fetchProjectAnswers(projectId),
      ProjectApi.fetchProjectIssues(projectId),
      ProjectApi.fetchProjectMemberships(projectId),
      ProjectApi.fetchProjectMembershipHierarchy(projectId),
      CatalogApi.fetchCatalogs(),
      ProjectApi.fetchProjectFiles(projectId)
    ])
      .then(([
        project, hierarchy, snapshots, views, answers, issues, memberships, membershipHierarchy, catalogs, files]) => {
        const projectData = {
          project,
          hierarchy,
          snapshots,
          views,
          answers,
          issues,
          memberships: [...memberships, ...membershipHierarchy],
          catalogs,
          files
        }

        dispatch(removeFromPending('fetchProject'))
        dispatch(actions.fetchProjectSuccess(projectData))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProject'))
        dispatch(actions.fetchProjectError(serializeError(error)))
        throw error
      })
  }
}

export function updateProject(data) {
  return function (dispatch, getState) {
    const state = getState()
    const id = data?.id ?? state.project?.project?.project?.id

    if (!id) {
      console.warn('No project ID available for update.')
      return
    }

    dispatch(addToPending('updateProject'))
    dispatch(actions.updateProjectInit())

    return ProjectApi.updateProject(id, data)
      .then(() =>
        Promise.all([
          ProjectApi.fetchProject(id),
          ProjectApi.fetchProjectHierarchy(id),
        ])
      )
      .then(([project, hierarchy]) => {
        dispatch(actions.updateProjectSuccess({ project, hierarchy }))
      })
      .catch((error) => {
        dispatch(actions.updateProjectError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProject')))
  }
}

export function deleteProject(id) {
  return function (dispatch) {
    const idToDelete = id ?? projectId

    dispatch(addToPending('deleteProject'))
    dispatch(actions.deleteProjectInit())

    return ProjectApi.deleteProject(idToDelete)
      .then(() => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(actions.deleteProjectSuccess(idToDelete))

        if (!id) {
          window.location.href = `${baseUrl}/projects/`
        }
      })
      .catch((error) => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(actions.deleteProjectError(serializeError(error)))
        throw error
      })
  }
}

// visibility

export function fetchProjectVisibility() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectVisibility'))
    dispatch(actions.fetchProjectVisibilityInit())

    return ProjectApi.fetchProjectVisibility(projectId)
      .then(visibility => {
        dispatch(actions.fetchProjectVisibilitySuccess(visibility))
      })
      .catch(error => {
        if (error?.status === 404) {
          dispatch(actions.fetchProjectVisibilitySuccess(null))
          return null
        }

        dispatch(actions.fetchProjectVisibilityError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectVisibility')))
  }
}

export function updateProjectVisibility(data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectVisibility'))
    dispatch(actions.updateProjectVisibilityInit())

    return ProjectApi.updateProjectVisibility(projectId, data)
      .then((visibility) => {
        dispatch(actions.updateProjectVisibilitySuccess(visibility))
      })
      .catch(error => {
        dispatch(actions.updateProjectVisibilityError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectVisibility')))
  }
}

export function deleteProjectVisibility() {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectVisibility'))
    dispatch(actions.deleteProjectVisibilityInit())

    return ProjectApi.deleteProjectVisibility(projectId)
      .then(() => {
        dispatch(fetchProjectVisibility())
        dispatch(actions.deleteProjectVisibilitySuccess())
      })
      .catch(error => {
        dispatch(actions.deleteProjectVisibilityError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('deleteProjectVisibility')))
  }
}

// project issue

export function fetchProjectIssues() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectIssues'))
    dispatch(actions.fetchProjectIssuesInit())

    return ProjectApi.fetchProjectIssues(projectId)
      .then((issues) => {
        dispatch(actions.fetchProjectIssuesSuccess(issues))
      })
      .catch((error) => {
        dispatch(actions.fetchProjectIssuesError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectIssues')))
  }
}

export function updateProjectIssue(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectIssue'))
    dispatch(actions.updateProjectIssueInit())

    return ProjectApi.updateProjectIssue(projectId, issueId, data)
      .then(() => dispatch(fetchProjectIssues()))
      .then(() => {
        dispatch(actions.updateProjectIssueSuccess())
      })
      .catch((error) => {
        dispatch(actions.updateProjectIssueError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectIssue')))
  }
}

// send project issue

export function sendProjectIssueEmail(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('sendProjectIssueEmail'))
    dispatch(actions.sendProjectIssueEmailInit())

    return ProjectApi.sendProjectIssueEmail(projectId, issueId, data)
      .then(() => {
        dispatch(actions.sendProjectIssueEmailSuccess())

        return dispatch(fetchProjectIssues())
          .catch(() => {})
      }, error => {
        dispatch(actions.sendProjectIssueEmailError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('sendProjectIssueEmail')))
  }
}

export function sendProjectIssueIntegration(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('sendProjectIssueIntegration'))
    dispatch(actions.sendProjectIssueIntegrationInit())

    return ProjectApi.sendProjectIssueIntegration(projectId, issueId, data)
      .then((response) => {
        dispatch(actions.sendProjectIssueIntegrationSuccess())

        if (response?.redirect_url) {
          dispatch(addToStale('projectIssues'))
          window.location.href = response.redirect_url
          return response
        }

        return dispatch(fetchProjectIssues())
          .catch(() => {})
          .then(() => response)
      }, error => {
        dispatch(actions.sendProjectIssueIntegrationError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('sendProjectIssueIntegration')))
  }
}

// memberships / invites / leave

export function fetchProjectInvites() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectInvites'))
    dispatch(actions.fetchProjectInvitesInit())

    return ProjectApi.fetchProjectInvites(projectId)
      .then(invites => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch(actions.fetchProjectInvitesSuccess(invites))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch(actions.fetchProjectInvitesError(serializeError(error)))
      })
  }
}

export function createProjectMember(data) {
  return function (dispatch) {
    dispatch(addToPending('createProjectMember'))
    dispatch(actions.createProjectMemberInit())

    return ProjectApi.createMember(projectId, data)
      .then(member => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch(actions.createProjectMemberSuccess(member))
      })
      .catch(error => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch(actions.createProjectMemberError(serializeError(error)))
        throw error
      })
  }
}

export function updateProjectMember(membershipId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectMember'))
    dispatch(actions.updateProjectMemberInit())

    return ProjectApi.updateMember(projectId, membershipId, data)
      .then(member => {
        dispatch(actions.updateProjectMemberSuccess({ ...member, id: membershipId }))

        // membership updates can lead to a permission change for owner <-> last owner cases
        // project with permissions needs to be fetched
        return ProjectApi.fetchProject(projectId)
      })
      .then((project) => {
        dispatch(actions.updateProjectSuccess({ project }))
      })
      .catch(error => {
        dispatch(actions.updateProjectMemberError(serializeError(error)))
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectMember')))
  }
}

export function deleteProjectMember(membershipId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectMember'))
    dispatch(actions.deleteProjectMemberInit())

    return ProjectApi.deleteMember(projectId, membershipId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch(actions.deleteProjectMemberSuccess(membershipId))
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch(actions.deleteProjectMemberError(serializeError(error)))
        throw error
      })
  }
}

export function sendProjectInvite(data) {
  return function (dispatch) {
    dispatch(addToPending('sendInvite'))
    dispatch(actions.sendInviteInit())

    return ProjectApi.sendInvite(projectId, data)
      .then(invite => {
        dispatch(removeFromPending('sendInvite'))
        dispatch(actions.sendInviteSuccess(invite))
      })
      .catch(error => {
        dispatch(removeFromPending('sendInvite'))
        dispatch(actions.sendInviteError(serializeError(error)))
        throw error
      })
  }
}

export function updateProjectInvite(inviteId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectInvite'))
    dispatch(actions.updateProjectInviteInit())

    return ProjectApi.updateInvite(projectId, inviteId, data)
      .then(invite => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch(actions.updateProjectInviteSuccess({ ...invite, id: inviteId }))
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch(actions.updateProjectInviteError(serializeError(error)))
        throw error
      })
  }
}

export function deleteProjectInvite(inviteId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectInvite'))
    dispatch(actions.deleteProjectInviteInit())

    return ProjectApi.deleteInvite(projectId, inviteId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch(actions.deleteProjectInviteSuccess(inviteId))
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch(actions.deleteProjectInviteError(serializeError(error)))
        throw error
      })
  }
}

export function leaveProject(membershipId, { redirect = false } = {}) {
  return function (dispatch) {
    dispatch(addToPending('leaveProject'))
    dispatch(actions.leaveProjectInit())

    return ProjectApi.leaveProject(projectId)
      .then(() => {
        dispatch(removeFromPending('leaveProject'))
        dispatch(actions.leaveProjectSuccess(membershipId))
        if (redirect) {
          window.location.href = `${baseUrl}/projects/`
          return
        }
      })
      .catch(error => {
        dispatch(removeFromPending('leaveProject'))
        dispatch(actions.leaveProjectError(serializeError(error)))
        throw error
      })
  }
}

// snapshots

export function createSnapshot(data) {
  return function (dispatch) {
    dispatch(addToPending('createSnapshot'))
    dispatch(actions.createSnapshotInit())

    return ProjectApi.createSnapshot(projectId, data)
      .then(snapshot => {
        dispatch(removeFromPending('createSnapshot'))
        dispatch(actions.createSnapshotSuccess(snapshot))
      })
      .catch(error => {
        dispatch(removeFromPending('createSnapshot'))
        dispatch(actions.createSnapshotError(serializeError(error)))
        throw error
      })
  }
}

export function updateSnapshot(snapshotId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateSnapshot'))
    dispatch(actions.updateSnapshotInit())

    return ProjectApi.updateSnapshot(projectId, snapshotId, data)
      .then(snapshot => {
        dispatch(removeFromPending('updateSnapshot'))
        dispatch(actions.updateSnapshotSuccess(snapshot))
      })
      .catch(error => {
        dispatch(removeFromPending('updateSnapshot'))
        dispatch(actions.updateSnapshotError(serializeError(error)))
        throw error
      })
  }
}

export function deleteSnapshot(snapshotId) {
  return function (dispatch) {
    dispatch(addToPending('deleteSnapshot'))
    dispatch(actions.deleteSnapshotInit())

    return ProjectApi.deleteSnapshot(projectId, snapshotId)
      .then(() => {
        dispatch(removeFromPending('deleteSnapshot'))
        dispatch(actions.deleteSnapshotSuccess(snapshotId))
      })
      .catch(error => {
        dispatch(removeFromPending('deleteSnapshot'))
        dispatch(actions.deleteSnapshotError(serializeError(error)))
        throw error
      })
  }
}

export function rollbackSnapshot(snapshotId) {
  return function (dispatch) {
    dispatch(addToPending('rollbackSnapshot'))
    dispatch(actions.rollbackSnapshotInit())

    return ProjectApi.rollbackSnapshot(projectId, snapshotId)
      .then(snapshot => {
        dispatch(removeFromPending('rollbackSnapshot'))
        dispatch(actions.rollbackSnapshotSuccess(snapshot))
        dispatch(fetchProject())
      })
      .catch(error => {
        dispatch(removeFromPending('rollbackSnapshot'))
        dispatch(actions.rollbackSnapshotError(serializeError(error)))
        throw error
      })
  }
}

// files

export function fetchProjectFiles(snapshotId) {
  const pendingId = isNil(snapshotId) ? 'fetchProjectFiles' : `fetchProjectFiles/${snapshotId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(actions.fetchProjectFilesInit())

    return ProjectApi.fetchProjectFiles(projectId, snapshotId)
      .then(files => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchProjectFilesSuccess(files))
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchProjectFilesError(serializeError(error)))
        throw error
      })
  }
}

// answers / views

export function fetchAnswers(snapshotId, params = {}) {
  const pendingId = isNil(snapshotId) ? 'fetchAnswers' : `fetchAnswers/${snapshotId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(actions.fetchAnswersInit())

    return ProjectApi.fetchProjectAnswers(projectId, snapshotId, params)
      .then(view => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchAnswersSuccess(view))
        return view
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchAnswersError(serializeError(error)))
        throw error
      })
  }
}

export function fetchView(snapshotId, viewId) {
  const pendingId = isNil(snapshotId) ? `fetchView/${viewId}` : `fetchView/${snapshotId}/${viewId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch(actions.fetchViewInit())

    return ProjectApi.fetchProjectView(projectId, snapshotId, viewId)
      .then(view => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchViewSuccess(view))
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchViewError(serializeError(error)))
      })
  }
}

// navigation

export function fetchNavigation() {
  const pendingId = 'fetchNavigation'

  return (dispatch) => {
    dispatch(addToPending(pendingId))
    dispatch(actions.fetchNavigationInit())

    return ProjectApi.fetchProjectNavigation(projectId)
      .then((navigation) => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchNavigationSuccess(navigation))
      })
      .catch((error) => {
        dispatch(removeFromPending(pendingId))
        dispatch(actions.fetchNavigationError(serializeError(error)))
      })
  }
}

// progress

export function fetchProgress() {
  return (dispatch) => {
    dispatch(addToPending('fetchProgress'))
    dispatch(actions.fetchProgressInit())

    return ProjectApi.fetchProjectProgress(projectId)
      .then((progress) => {
        dispatch(removeFromPending('fetchProgress'))
        dispatch(actions.fetchProgressSuccess(progress))
      })
      .catch((error) => {
        dispatch(removeFromPending('fetchProgress'))
        dispatch(actions.fetchProgressError(serializeError(error)))
      })
  }
}

// download

export function downloadAnswers(snapshotId, format, params = {}) {
  return function (dispatch) {
    dispatch(addToPending('downloadAnswers'))
    dispatch(actions.downloadAnswersInit())

    return ProjectApi.downloadProjectAnswers(projectId, snapshotId, format, params)
      .then(() => dispatch(actions.downloadAnswersSuccess()))
      .catch(error => dispatch(actions.downloadAnswersError(serializeError(error))))
      .finally(() => dispatch(removeFromPending('downloadAnswers')))
  }
}

export function downloadView(snapshotId, viewId, format) {
  return function (dispatch) {
    dispatch(addToPending('downloadView'))
    dispatch(actions.downloadViewInit())

    return ProjectApi.downloadProjectView(projectId, snapshotId, viewId, format)
      .then(() => dispatch(actions.downloadViewSuccess()))
      .catch(error => dispatch(actions.downloadViewError(serializeError(error))))
      .finally(() => dispatch(removeFromPending('downloadView')))
  }
}

// providers

export function fetchProviders() {
  return function (dispatch) {
    dispatch(addToPending('fetchProviders'))
    dispatch(actions.fetchProvidersInit())

    return ProjectApi.fetchProviders()
      .then(providers => {
        dispatch(removeFromPending('fetchProviders'))
        dispatch(actions.fetchProvidersSuccess(providers))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProviders'))
        dispatch(actions.fetchProvidersError(serializeError(error)))
        throw error
      })
  }
}

// integrations

export function fetchProjectIntegrations() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectIntegrations'))
    dispatch(actions.fetchProjectIntegrationsInit())

    return ProjectApi.fetchProjectIntegrations(projectId)
      .then(integrations => {
        dispatch(removeFromPending('fetchProjectIntegrations'))
        dispatch(actions.fetchProjectIntegrationsSuccess(integrations))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectIntegrations'))
        dispatch(actions.fetchProjectIntegrationsError(serializeError(error)))
        throw error
      })
  }
}

export function createProjectIntegration(data) {
  return function (dispatch) {
    dispatch(addToPending('createProjectIntegration'))
    dispatch(actions.createProjectIntegrationInit())

    return ProjectApi.createProjectIntegration(projectId, data)
      .then(integration => {
        dispatch(removeFromPending('createProjectIntegration'))
        dispatch(actions.createProjectIntegrationSuccess(integration))
      })
      .catch(error => {
        dispatch(removeFromPending('createProjectIntegration'))
        dispatch(actions.createProjectIntegrationError(serializeError(error)))
        throw error
      })
  }
}

export function updateProjectIntegration(integrationId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectIntegration'))
    dispatch(actions.updateProjectIntegrationInit())

    return ProjectApi.updateProjectIntegration(projectId, integrationId, data)
      .then(integration => {
        dispatch(removeFromPending('updateProjectIntegration'))
        dispatch(actions.updateProjectIntegrationSuccess(integration))
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectIntegration'))
        dispatch(actions.updateProjectIntegrationError(serializeError(error)))
        throw error
      })
  }
}

export function deleteProjectIntegration(integrationId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectIntegration'))
    dispatch(actions.deleteProjectIntegrationInit())

    return ProjectApi.deleteProjectIntegration(projectId, integrationId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectIntegration'))
        dispatch(actions.deleteProjectIntegrationSuccess(integrationId))
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectIntegration'))
        dispatch(actions.deleteProjectIntegrationError(serializeError(error)))
        throw error
      })
  }
}

// synchronous actions

export function clearProjectErrors() {
  return actions.clearProjectErrors()
}

export function clearCurrentView() {
  return actions.clearCurrentView()
}

export function setProjectAnswers(view) {
  return function (dispatch) {
    dispatch(actions.setProjectAnswers(view))
  }
}
