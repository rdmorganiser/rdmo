import { encodeParams } from 'rdmo/core/assets/js/utils/api'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

export default class ProjectApi extends BaseApi {

  static fetchProject(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/`)
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
    return this.get(`/api/v1/projects/projects/${projectId}/memberships/hierarchy`)
  }

  static fetchProjectInvites(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/invites/`)
  }

  static fetchViews() {
    return this.get('/api/v1/projects/views/views/')
  }

  static fetchProjects(params) {
    return this.get(`/api/v1/projects/projects/?${encodeParams(params)}`)
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
}
