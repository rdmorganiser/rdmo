import ProjectApi from '../api/ProjectApi'
import CatalogsApi from '/rdmo/projects/assets/js/common/api/CatalogsApi'

import { projectId } from '../utils/meta'

import {
  FETCH_PROJECT_INIT,
  FETCH_PROJECT_SUCCESS,
  FETCH_PROJECT_ERROR,
  UPDATE_PROJECT_INIT,
  UPDATE_PROJECT_SUCCESS,
  UPDATE_PROJECT_ERROR,
  DELETE_PROJECT_INIT,
  DELETE_PROJECT_SUCCESS,
  DELETE_PROJECT_ERROR,
  FETCH_PROJECT_INVITES_INIT,
  FETCH_PROJECT_INVITES_SUCCESS,
  FETCH_PROJECT_INVITES_ERROR,
  ADD_PROJECT_MEMBER_INIT,
  ADD_PROJECT_MEMBER_SUCCESS,
  ADD_PROJECT_MEMBER_ERROR,
  SEND_INVITE_INIT,
  SEND_INVITE_SUCCESS,
  SEND_INVITE_ERROR
} from './actionTypes'

import { addToPending, removeFromPending } from 'rdmo/core/assets/js/actions/pendingActions'
import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { updateLocation } from '../utils/location'

export function setPage(page) {
  return function(dispatch) {
    dispatch(updateConfig('page', page))
    updateLocation(page)
  }
}

export function fetchProject() {
  return function(dispatch) {
    dispatch(addToPending('fetchProject'))
    dispatch(fetchProjectInit())

    return Promise.all([
      ProjectApi.fetchProject(projectId),
      ProjectApi.fetchProjectSnapshots(projectId),
      ProjectApi.fetchProjectTasks(projectId),
      ProjectApi.fetchProjectMemberships(projectId),
      CatalogsApi.fetchCatalogs()
    ])
    .then(([project, snapshots, tasks, memberships, catalogs]) => {
      // project.snapshots = snapshots
      // project.tasks = tasks
      const projectData = {
        project: project,
        snapshots: snapshots,
        tasks: tasks,
        memberships: memberships,
        catalogs: catalogs
      }

      dispatch(removeFromPending('fetchProject'))
      dispatch(fetchProjectSuccess(projectData))
    })
    .catch(error => {
      dispatch(removeFromPending('fetchProject'))
      dispatch(fetchProjectError(error))
      throw error
    })
  }
}

export function fetchProjectInit() {
  return {type: FETCH_PROJECT_INIT}
}

export function fetchProjectSuccess(project) {
  return {type: FETCH_PROJECT_SUCCESS, project}
}

export function fetchProjectError(error) {
  return {type: FETCH_PROJECT_ERROR, error}
}

export function updateProject(data) {
  return function (dispatch, getState) {
    const state = getState()
    const currentBundle = state.project.project
    const id = currentBundle?.project?.id

    if (!id) {
      console.warn('No project ID available for update.')
      return
    }

    dispatch(addToPending('updateProject'))
    dispatch(updateProjectInit())

    return ProjectApi.updateProject(id, data)
      .then((updatedProject) => {
        const updatedBundle = {
          ...currentBundle,
          project: updatedProject
        }

        dispatch(removeFromPending('updateProject'))
        dispatch(updateProjectSuccess(updatedBundle))
      })
      .catch((error) => {
        dispatch(removeFromPending('updateProject'))
        dispatch(updateProjectError(error))
        throw error
      })
  }
}

export function updateProjectInit() {
  return { type: UPDATE_PROJECT_INIT }
}

export function updateProjectSuccess(project) {
  return { type: UPDATE_PROJECT_SUCCESS, project }
}

export function updateProjectError(error) {
  return { type: UPDATE_PROJECT_ERROR, error }
}

export function deleteProject(projectId) {
  return function (dispatch) {
    dispatch(addToPending('deleteProject'))
    dispatch(deleteProjectInit())

    return ProjectApi.deleteProject(projectId)
      .then(() => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(deleteProjectSuccess(projectId))
      })
      .catch((error) => {
        dispatch(removeFromPending('deleteProject'))
        dispatch(deleteProjectError(error))
        throw error
      })
  }
}

export function deleteProjectInit() {
  return { type: DELETE_PROJECT_INIT }
}

export function deleteProjectSuccess(projectId) {
  return { type: DELETE_PROJECT_SUCCESS, projectId }
}

export function deleteProjectError(error) {
  return { type: DELETE_PROJECT_ERROR, error }
}

export function fetchProjectInvites(projectId) {
  return function(dispatch) {
    dispatch(addToPending('fetchProjectInvites'))
    dispatch(fetchProjectInvitesInit())

    return ProjectApi.fetchProjectInvites(projectId)
      .then(invites => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch(fetchProjectInvitesSuccess(invites))
      })
      .catch(error => {
        dispatch(removeFromPending('fetchProjectInvites'))
        dispatch(fetchProjectInvitesError(error))
      })
  }
}

export function fetchProjectInvitesInit() {
  return {type: FETCH_PROJECT_INVITES_INIT}
}

export function fetchProjectInvitesSuccess(invites) {
  return {type: FETCH_PROJECT_INVITES_SUCCESS, invites}
}

export function fetchProjectInvitesError(error) {
  return {type: FETCH_PROJECT_INVITES_ERROR, error}
}

export function addProjectMember(data) {
  return function(dispatch) {
    dispatch(addToPending('addProjectMember'))
    dispatch(addProjectMemberInit())

    return ProjectApi.addMember(projectId, data)
      .then(member => {
        dispatch(removeFromPending('addProjectMember'))
        dispatch(addProjectMemberSuccess(member))
      })
      .catch(error => {
        dispatch(removeFromPending('addProjectMember'))
        dispatch(addProjectMemberError(error))
        throw error
      })
  }
}

export function addProjectMemberInit() {
  return {type: ADD_PROJECT_MEMBER_INIT}
}

export function addProjectMemberSuccess(member) {
  return {type: ADD_PROJECT_MEMBER_SUCCESS, member}
}

export function addProjectMemberError(error) {
  return {type: ADD_PROJECT_MEMBER_ERROR, error}
}

export function sendProjectInvite(data) {
  return function(dispatch) {
    dispatch(addToPending('sendInvite'))
    dispatch(sendProjectInviteInit())

    return ProjectApi.sendInvite(projectId, data)
      .then(invite => {
        dispatch(removeFromPending('sendInvite'))
        dispatch(sendProjectInviteSuccess(invite))
      })
      .catch(error => {
        dispatch(removeFromPending('sendInvite'))
        dispatch(sendProjectInviteError(error))
        throw error
      })
  }
}

export function sendProjectInviteInit() {
  return {type: SEND_INVITE_INIT}
}

export function sendProjectInviteSuccess(invite) {
  return {type: SEND_INVITE_SUCCESS, invite}
}

export function sendProjectInviteError(error) {
  return {type: SEND_INVITE_ERROR, error}
}
