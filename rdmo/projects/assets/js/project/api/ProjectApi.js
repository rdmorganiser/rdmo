import { isNil } from 'lodash'

import { encodeParams } from 'rdmo/core/assets/js/utils/api'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

export default class ProjectApi extends BaseApi {

  static fetchProject(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/`)
  }

  static fetchProjectHierarchy(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/hierarchy/`)
  }

  static fetchProjectSnapshots(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/snapshots/`)
  }

  static fetchProjectTasks(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/issues/`)
  }

  static fetchProjectMemberships(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/memberships/`)
  }

  static fetchProjectMembershipHierarchy(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/memberships/hierarchy/`)
  }

  static fetchProjectInvites(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/invites/`)
  }

  static fetchProjects(params) {
    return this.get(`/api/v1/projects/projects/?${encodeParams(params)}`)
  }

  static createProject(data) {
    return this.post('/api/v1/projects/projects/', data)
  }

  static updateProject(projectId, data) {
    return this.put(`/api/v1/projects/projects/${projectId}/`, data)
  }

  static deleteProject(projectId) {
    return this.delete(`/api/v1/projects/projects/${projectId}/`)
  }

  static createMember(projectId, data) {
    return this.post(`/api/v1/projects/projects/${projectId}/memberships/`, data)
  }

  static updateMember(projectId, membershipId, data) {
    return this.put(`/api/v1/projects/projects/${projectId}/memberships/${membershipId}/`, data)
  }

  static deleteMember(projectId, membershipId) {
    return this.delete(`/api/v1/projects/projects/${projectId}/memberships/${membershipId}/`)
  }

  static leaveProject(projectId) {
    return this.delete(`/api/v1/projects/projects/${projectId}/memberships/leave/`)
  }

  static sendInvite(projectId, data) {
    return this.post(`/api/v1/projects/projects/${projectId}/invites/`, data)
  }

  static updateInvite(projectId, inviteId, data) {
    return this.put(`/api/v1/projects/projects/${projectId}/invites/${inviteId}/`, data)
  }

  static deleteInvite(projectId, inviteId) {
    return this.delete(`/api/v1/projects/projects/${projectId}/invites/${inviteId}/`)
  }

  static createSnapshot(projectId, data) {
    return this.post(`/api/v1/projects/projects/${projectId}/snapshots/`, data)
  }

  static updateSnapshot(projectId, snapshotId, data) {
    return this.put(`/api/v1/projects/projects/${projectId}/snapshots/${snapshotId}/`, data)
  }

  static deleteSnapshot(projectId, snapshotId) {
    return this.delete(`/api/v1/projects/projects/${projectId}/snapshots/${snapshotId}/`)
  }

  static rollbackSnapshot(projectId, snapshotId) {
    return this.post(`/api/v1/projects/projects/${projectId}/snapshots/${snapshotId}/rollback/`)
  }

  static fetchProjectAnswers(projectId, snapshotId) {
    if (isNil(snapshotId)) {
      return this.get(`/api/v1/projects/projects/${projectId}/answers/`)
    } else {
      return this.get(`/api/v1/projects/projects/${projectId}/snapshots/${snapshotId}/answers/`)
    }
  }

  static downloadProjectAnswers(projectId, snapshotId, format) {
    if (isNil(snapshotId)) {
      return this.download(`/api/v1/projects/projects/${projectId}/answers/export/${format}/`)
    } else {
      return this.download(`/api/v1/projects/projects/${projectId}/snapshots/${snapshotId}/answers/export/${format}/`)
    }
  }

  static fetchProjectViews(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/views/`)
  }

  static fetchProjectView(projectId, snapshotId, viewId) {
    if (isNil(snapshotId)) {
      return this.get(`/api/v1/projects/projects/${projectId}/views/${viewId}/`)
    } else {
      return this.get(`/api/v1/projects/projects/${projectId}/snapshots/${snapshotId}/views/${viewId}/`)
    }
  }

  static downloadProjectView(projectId, snapshotId, viewId, format) {
    if (isNil(snapshotId)) {
      return this.download(`/api/v1/projects/projects/${projectId}/views/${viewId}/export/${format}/`)
    } else {
      return this.download(`/api/v1/projects/projects/${projectId}/snapshots/${snapshotId}/views/${viewId}/export/${format}/`)
    }
  }
}
