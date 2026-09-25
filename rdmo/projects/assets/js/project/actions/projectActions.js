import { isNil } from 'lodash'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import CatalogApi from 'rdmo/projects/assets/js/common/api/CatalogApi'

import { projectId } from '../utils/meta'

import ProjectApi from '../api/ProjectApi'

import * as actionTypes from './actionTypes'

// asynchronous actions

// project

export function fetchProject() {

  return function (dispatch) {
    dispatch(addToPending('fetchProject'))
    dispatch({ type: actionTypes.FETCH_PROJECT_INIT })

    return Promise.all([
      ProjectApi.fetchProject(projectId),
      ProjectApi.fetchProjectHierarchy(projectId),
      ProjectApi.fetchProjectSnapshots(projectId),
      ProjectApi.fetchProjectViews(projectId),
      ProjectApi.fetchProjectAnswers(projectId),
      ProjectApi.fetchProjectTasks(projectId),
      ProjectApi.fetchProjectMemberships(projectId),
      ProjectApi.fetchProjectMembershipHierarchy(projectId),
      CatalogApi.fetchCatalogs(),
      ProjectApi.fetchProjectFiles(projectId)
    ])
      .then(([
        project, hierarchy, snapshots, views, answers, tasks, memberships, membershipHierarchy, catalogs, files]) => {
        const projectData = {
          project,
          hierarchy,
          snapshots,
          views,
          answers,
          tasks,
          memberships: [...memberships, ...membershipHierarchy],
          catalogs,
          files
        }

        dispatch(removeFromPending('fetchProject'))
        dispatch({ type: actionTypes.FETCH_PROJECT_SUCCESS, project: projectData })
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProject'))
        dispatch({ type: actionTypes.FETCH_PROJECT_ERROR, error })
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
    dispatch({ type: actionTypes.UPDATE_PROJECT_INIT })

    return ProjectApi.updateProject(id, data)
      .then(() =>
        Promise.all([
          ProjectApi.fetchProject(id),
          ProjectApi.fetchProjectHierarchy(id),
        ])
      )
      .then(([project, hierarchy]) => {
        dispatch({
          type: actionTypes.UPDATE_PROJECT_SUCCESS,
          project: { project, hierarchy }
        })
      })
      .catch((error) => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProject')))
  }
}

export function deleteProject(id) {
  return function (dispatch) {
    const idToDelete = id ?? projectId

    dispatch(addToPending('deleteProject'))
    dispatch({ type: actionTypes.DELETE_PROJECT_INIT })

    return ProjectApi.deleteProject(idToDelete)
      .then(() => {
        dispatch(removeFromPending('deleteProject'))
        dispatch({ type: actionTypes.DELETE_PROJECT_SUCCESS, projectId: idToDelete })

        if (!id) {
          window.location.href = `${baseUrl}/projects/`
        }
      })
      .catch((error) => {
        dispatch(removeFromPending('deleteProject'))
        dispatch({ type: actionTypes.DELETE_PROJECT_ERROR, error })
        throw error
      })
  }
}

// visibility

export function fetchProjectVisibility() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectVisibility'))
    dispatch({ type: actionTypes.FETCH_PROJECT_VISIBILITY_INIT })

    return ProjectApi.fetchProjectVisibility(projectId)
      .then(visibility => {
        dispatch({ type: actionTypes.FETCH_PROJECT_VISIBILITY_SUCCESS, visibility })
      })
      .catch(error => {
        if (error?.status === 404) {
          dispatch({ type: actionTypes.FETCH_PROJECT_VISIBILITY_SUCCESS, visibility: null })
          return null
        }

        dispatch({ type: actionTypes.FETCH_PROJECT_VISIBILITY_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectVisibility')))
  }
}

export function updateProjectVisibility(data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectVisibility'))
    dispatch({ type: actionTypes.UPDATE_PROJECT_VISIBILITY_INIT })

    return ProjectApi.updateProjectVisibility(projectId, data)
      .then((visibility) => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_VISIBILITY_SUCCESS, visibility })
      })
      .catch(error => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_VISIBILITY_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectVisibility')))
  }
}

export function deleteProjectVisibility() {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectVisibility'))
    dispatch({ type: actionTypes.DELETE_PROJECT_VISIBILITY_INIT })

    return ProjectApi.deleteProjectVisibility(projectId)
      .then(() => {
        dispatch(fetchProjectVisibility())
        dispatch({ type: actionTypes.DELETE_PROJECT_VISIBILITY_SUCCESS })
      })
      .catch(error => {
        dispatch({ type: actionTypes.DELETE_PROJECT_VISIBILITY_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('deleteProjectVisibility')))
  }
}

// project task

export function fetchProjectTasks() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectTasks'))
    dispatch({ type: actionTypes.FETCH_PROJECT_TASKS_INIT })

    return ProjectApi.fetchProjectTasks(projectId)
      .then((tasks) => {
        dispatch({ type: actionTypes.FETCH_PROJECT_TASKS_SUCCESS, tasks })
      })
      .catch((error) => {
        dispatch({ type: actionTypes.FETCH_PROJECT_TASKS_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('fetchProjectTasks')))
  }
}

export function updateProjectTask(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectTask'))
    dispatch({ type: actionTypes.UPDATE_PROJECT_TASK_INIT })

    return ProjectApi.updateProjectTask(projectId, issueId, data)
      .then(() => dispatch(fetchProjectTasks()))
      .then(() => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_TASK_SUCCESS })
      })
      .catch((error) => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_TASK_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectTask')))
  }
}

// send project issue

export function sendProjectIssueEmail(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('sendProjectIssueEmail'))
    dispatch({ type: actionTypes.SEND_PROJECT_ISSUE_EMAIL_INIT })

    return ProjectApi.sendProjectIssueEmail(projectId, issueId, data)
      .then(() => {
        dispatch({ type: actionTypes.SEND_PROJECT_ISSUE_EMAIL_SUCCESS })
        dispatch(fetchProjectTasks())
      })
      .catch(error => {
        dispatch({ type: actionTypes.SEND_PROJECT_ISSUE_EMAIL_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('sendProjectIssueEmail')))
  }
}

export function sendProjectIssueIntegration(issueId, data) {
  return function (dispatch) {
    dispatch(addToPending('sendProjectIssueIntegration'))
    dispatch({ type: actionTypes.SEND_PROJECT_ISSUE_INTEGRATION_INIT })

    return ProjectApi.sendProjectIssueIntegration(projectId, issueId, data)
      .then((response) => {
        dispatch({ type: actionTypes.SEND_PROJECT_ISSUE_INTEGRATION_SUCCESS })
        dispatch(fetchProjectTasks())

        if (response?.redirect_url) {
          window.location.href = response.redirect_url
        }

        return response
      })
      .catch(error => {
        dispatch({ type: actionTypes.SEND_PROJECT_ISSUE_INTEGRATION_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('sendProjectIssueIntegration')))
  }
}

// memberships / invites / leave

export function fetchProjectInvites() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectInvites'))
    dispatch({ type: actionTypes.FETCH_PROJECT_INVITES_INIT })

    return ProjectApi.fetchProjectInvites(projectId)
      .then(invites => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch({ type: actionTypes.FETCH_PROJECT_INVITES_SUCCESS, invites })
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch({ type: actionTypes.FETCH_PROJECT_INVITES_ERROR, error })
      })
  }
}

export function createProjectMember(data) {
  return function (dispatch) {
    dispatch(addToPending('createProjectMember'))
    dispatch({ type: actionTypes.CREATE_PROJECT_MEMBER_INIT })

    return ProjectApi.createMember(projectId, data)
      .then(member => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch({ type: actionTypes.CREATE_PROJECT_MEMBER_SUCCESS, member })
      })
      .catch(error => {
        dispatch(removeFromPending('createProjectMember'))
        dispatch({ type: actionTypes.CREATE_PROJECT_MEMBER_ERROR, error })
        throw error
      })
  }
}

export function updateProjectMember(membershipId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectMember'))
    dispatch({ type: actionTypes.UPDATE_PROJECT_MEMBER_INIT })

    return ProjectApi.updateMember(projectId, membershipId, data)
      .then(member => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_MEMBER_SUCCESS, member: { ...member, id: membershipId } })

        // membership updates can lead to a permission change for owner <-> last owner cases
        // project with permissions needs to be fetched
        return ProjectApi.fetchProject(projectId)
      })
      .then((project) => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_SUCCESS, project: { project } })
      })
      .catch(error => {
        dispatch({ type: actionTypes.UPDATE_PROJECT_MEMBER_ERROR, error })
        throw error
      })
      .finally(() => dispatch(removeFromPending('updateProjectMember')))
  }
}

export function deleteProjectMember(membershipId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectMember'))
    dispatch({ type: actionTypes.DELETE_PROJECT_MEMBER_INIT })

    return ProjectApi.deleteMember(projectId, membershipId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch({ type: actionTypes.DELETE_PROJECT_MEMBER_SUCCESS, membershipId })
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectMember'))
        dispatch({ type: actionTypes.DELETE_PROJECT_MEMBER_ERROR, error })
        throw error
      })
  }
}

export function sendProjectInvite(data) {
  return function (dispatch) {
    dispatch(addToPending('sendInvite'))
    dispatch({ type: actionTypes.SEND_INVITE_INIT })

    return ProjectApi.sendInvite(projectId, data)
      .then(invite => {
        dispatch(removeFromPending('sendInvite'))
        dispatch({ type: actionTypes.SEND_INVITE_SUCCESS, invite })
      })
      .catch(error => {
        dispatch(removeFromPending('sendInvite'))
        dispatch({ type: actionTypes.SEND_INVITE_ERROR, error })
        throw error
      })
  }
}

export function updateProjectInvite(inviteId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectInvite'))
    dispatch({ type: actionTypes.UPDATE_PROJECT_INVITE_INIT })

    return ProjectApi.updateInvite(projectId, inviteId, data)
      .then(invite => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_INVITE_SUCCESS, invite: { ...invite, id: inviteId } })
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectInvite'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_INVITE_ERROR, error })
        throw error
      })
  }
}

export function deleteProjectInvite(inviteId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectInvite'))
    dispatch({ type: actionTypes.DELETE_PROJECT_INVITE_INIT })

    return ProjectApi.deleteInvite(projectId, inviteId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch({ type: actionTypes.DELETE_PROJECT_INVITE_SUCCESS, inviteId })
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectInvite'))
        dispatch({ type: actionTypes.DELETE_PROJECT_INVITE_ERROR, error })
        throw error
      })
  }
}

export function leaveProject(membershipId, { redirect = false } = {}) {
  return function (dispatch) {
    dispatch(addToPending('leaveProject'))
    dispatch({ type: actionTypes.LEAVE_PROJECT_INIT })

    return ProjectApi.leaveProject(projectId)
      .then(() => {
        dispatch(removeFromPending('leaveProject'))
        dispatch({ type: actionTypes.LEAVE_PROJECT_SUCCESS, membershipId })
        if (redirect) {
          window.location.href = `${baseUrl}/projects/`
          return
        }
      })
      .catch(error => {
        dispatch(removeFromPending('leaveProject'))
        dispatch({ type: actionTypes.LEAVE_PROJECT_ERROR, error })
        throw error
      })
  }
}

// snapshots

export function createSnapshot(data) {
  return function (dispatch) {
    dispatch(addToPending('createSnapshot'))
    dispatch({ type: actionTypes.CREATE_SNAPSHOT_INIT })

    return ProjectApi.createSnapshot(projectId, data)
      .then(snapshot => {
        dispatch(removeFromPending('createSnapshot'))
        dispatch({ type: actionTypes.CREATE_SNAPSHOT_SUCCESS, snapshot })
      })
      .catch(error => {
        dispatch(removeFromPending('createSnapshot'))
        dispatch({ type: actionTypes.CREATE_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

export function updateSnapshot(snapshotId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateSnapshot'))
    dispatch({ type: actionTypes.UPDATE_SNAPSHOT_INIT })

    return ProjectApi.updateSnapshot(projectId, snapshotId, data)
      .then(snapshot => {
        dispatch(removeFromPending('updateSnapshot'))
        dispatch({ type: actionTypes.UPDATE_SNAPSHOT_SUCCESS, snapshot })
      })
      .catch(error => {
        dispatch(removeFromPending('updateSnapshot'))
        dispatch({ type: actionTypes.UPDATE_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

export function deleteSnapshot(snapshotId) {
  return function (dispatch) {
    dispatch(addToPending('deleteSnapshot'))
    dispatch({ type: actionTypes.DELETE_SNAPSHOT_INIT })

    return ProjectApi.deleteSnapshot(projectId, snapshotId)
      .then(() => {
        dispatch(removeFromPending('deleteSnapshot'))
        dispatch({ type: actionTypes.DELETE_SNAPSHOT_SUCCESS, snapshotId })
      })
      .catch(error => {
        dispatch(removeFromPending('deleteSnapshot'))
        dispatch({ type: actionTypes.DELETE_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

export function rollbackSnapshot(snapshotId) {
  return function (dispatch) {
    dispatch(addToPending('rollbackSnapshot'))
    dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_INIT })

    return ProjectApi.rollbackSnapshot(projectId, snapshotId)
      .then(snapshot => {
        dispatch(removeFromPending('rollbackSnapshot'))
        dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_SUCCESS, snapshot })
        dispatch(fetchProject())
      })
      .catch(error => {
        dispatch(removeFromPending('rollbackSnapshot'))
        dispatch({ type: actionTypes.ROLLBACK_SNAPSHOT_ERROR, error })
        throw error
      })
  }
}

// files

export function fetchProjectFiles(snapshotId) {
  const pendingId = isNil(snapshotId) ? 'fetchProjectFiles' : `fetchProjectFiles/${snapshotId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch({ type: actionTypes.FETCH_PROJECT_FILES_INIT })

    return ProjectApi.fetchProjectFiles(projectId, snapshotId)
      .then(files => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_PROJECT_FILES_SUCCESS, files })
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_PROJECT_FILES_ERROR, error })
        throw error
      })
  }
}

// answers / views

export function fetchAnswers(snapshotId) {
  const pendingId = isNil(snapshotId) ? 'fetchAnswers' : `fetchView/${snapshotId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch({ type: actionTypes.FETCH_ANSWERS_INIT })

    return ProjectApi.fetchProjectAnswers(projectId, snapshotId)
      .then(view => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_ANSWERS_SUCCESS, view })
        return view
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_ANSWERS_ERROR, error })
        throw error
      })
  }
}

export function fetchView(snapshotId, viewId) {
  const pendingId = isNil(snapshotId) ? `fetchView/${viewId}` : `fetchView/${snapshotId}/${viewId}`

  return function (dispatch) {
    dispatch(addToPending(pendingId))
    dispatch({ type: actionTypes.FETCH_VIEW_INIT })

    return ProjectApi.fetchProjectView(projectId, snapshotId, viewId)
      .then(view => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_VIEW_SUCCESS, view })
      })
      .catch(error => {
        dispatch(removeFromPending(pendingId))
        dispatch({ type: actionTypes.FETCH_VIEW_ERROR, error })
      })
  }
}

// download

export function downloadAnswers(snapshotId, format) {
  return function (dispatch) {
    dispatch(addToPending('downloadAnswers'))
    dispatch({ type: actionTypes.DOWNLOAD_ANSWERS_INIT })

    return ProjectApi.downloadProjectAnswers(projectId, snapshotId, format)
      .then(() => dispatch({ type: actionTypes.DOWNLOAD_ANSWERS_SUCCESS }))
      .catch(error => dispatch({ type: actionTypes.DOWNLOAD_ANSWERS_ERROR, error }))
      .finally(() => dispatch(removeFromPending('downloadAnswers')))
  }
}

export function downloadView(snapshotId, viewId, format) {
  return function (dispatch) {
    dispatch(addToPending('downloadView'))
    dispatch({ type: actionTypes.DOWNLOAD_VIEW_INIT })

    return ProjectApi.downloadProjectView(projectId, snapshotId, viewId, format)
      .then(() => dispatch({ type: actionTypes.DOWNLOAD_VIEW_SUCCESS }))
      .catch(error => dispatch({ type: actionTypes.DOWNLOAD_VIEW_ERROR, error }))
      .finally(() => dispatch(removeFromPending('downloadView')))
  }
}

// providers

export function fetchProviders() {
  return function (dispatch) {
    dispatch(addToPending('fetchProviders'))
    dispatch({ type: actionTypes.FETCH_PROVIDERS_INIT })

    return ProjectApi.fetchProviders()
      .then(providers => {
        dispatch(removeFromPending('fetchProviders'))
        dispatch({ type: actionTypes.FETCH_PROVIDERS_SUCCESS, providers })
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProviders'))
        dispatch({ type: actionTypes.FETCH_PROVIDERS_ERROR, error })
        throw error
      })
  }
}

// integrations

export function fetchProjectIntegrations() {
  return function (dispatch) {
    dispatch(addToPending('fetchProjectIntegrations'))
    dispatch({ type: actionTypes.FETCH_PROJECT_INTEGRATIONS_INIT })

    return ProjectApi.fetchProjectIntegrations(projectId)
      .then(integrations => {
        dispatch(removeFromPending('fetchProjectIntegrations'))
        dispatch({ type: actionTypes.FETCH_PROJECT_INTEGRATIONS_SUCCESS, integrations })
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectIntegrations'))
        dispatch({ type: actionTypes.FETCH_PROJECT_INTEGRATIONS_ERROR, error })
        throw error
      })
  }
}

export function createProjectIntegration(data) {
  return function (dispatch) {
    dispatch(addToPending('createProjectIntegration'))
    dispatch({ type: actionTypes.CREATE_PROJECT_INTEGRATION_INIT })

    return ProjectApi.createProjectIntegration(projectId, data)
      .then(integration => {
        dispatch(removeFromPending('createProjectIntegration'))
        dispatch({ type: actionTypes.CREATE_PROJECT_INTEGRATION_SUCCESS, integration })
      })
      .catch(error => {
        dispatch(removeFromPending('createProjectIntegration'))
        dispatch({ type: actionTypes.CREATE_PROJECT_INTEGRATION_ERROR, error })
        throw error
      })
  }
}

export function updateProjectIntegration(integrationId, data) {
  return function (dispatch) {
    dispatch(addToPending('updateProjectIntegration'))
    dispatch({ type: actionTypes.UPDATE_PROJECT_INTEGRATION_INIT })

    return ProjectApi.updateProjectIntegration(projectId, integrationId, data)
      .then(integration => {
        dispatch(removeFromPending('updateProjectIntegration'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_INTEGRATION_SUCCESS, integration })
      })
      .catch(error => {
        dispatch(removeFromPending('updateProjectIntegration'))
        dispatch({ type: actionTypes.UPDATE_PROJECT_INTEGRATION_ERROR, error })
        throw error
      })
  }
}

export function deleteProjectIntegration(integrationId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProjectIntegration'))
    dispatch({ type: actionTypes.DELETE_PROJECT_INTEGRATION_INIT })

    return ProjectApi.deleteProjectIntegration(projectId, integrationId)
      .then(() => {
        dispatch(removeFromPending('deleteProjectIntegration'))
        dispatch({ type: actionTypes.DELETE_PROJECT_INTEGRATION_SUCCESS, integrationId })
      })
      .catch(error => {
        dispatch(removeFromPending('deleteProjectIntegration'))
        dispatch({ type: actionTypes.DELETE_PROJECT_INTEGRATION_ERROR, error })
        throw error
      })
  }
}

// synchronous actions

export function clearProjectErrors() {
  return { type: actionTypes.CLEAR_PROJECT_ERRORS }
}

export function clearCurrentView() {
  return { type: actionTypes.CLEAR_CURRENT_VIEW }
}

export function setProjectAnswers(view) {
  return function (dispatch) {
    dispatch({ type: actionTypes.SET_PROJECT_ANSWERS, view })
  }
}
