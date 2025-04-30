import { encodeParams } from 'rdmo/core/assets/js/utils/api'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

export default class ProjectApi extends BaseApi {

  static fetchProject(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/`)
  }

  // static fetchProject(projectId) {
  //   return this.get(`/api/v1/projects/projects/${projectId}/`).then(project => {
  //     console.log('Fetched project:', project)
  //     if (project && project.snapshots) {
  //       const snapshotsUrl = `/api/v1/projects/snapshots/?project=${projectId}`
  //       console.log('Fetching all snapshots for project from:', snapshotsUrl)

  //       return this.get(snapshotsUrl).then(snapshots => {
  //         project.snapshots = snapshots
  //         return project
  //       })
  //     }
  //     return project
  //   }).catch(error => {
  //     console.error('Error in fetching project or snapshots:', error)
  //     throw error
  //   })
  // }

  static fetchProjectSnapshots(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/snapshots/`)
  }

  static fetchProjectTasks(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/issues/`)
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
}
