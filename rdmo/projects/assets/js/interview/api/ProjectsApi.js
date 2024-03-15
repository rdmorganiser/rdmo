import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ProjectsApi extends BaseApi {

  static fetchProject(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/`)
  }

  static fetchOverview(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/overview/`)
  }

  static fetchNavigation(projectId, page_id) {
    return this.get(`/api/v1/projects/projects/${projectId}/navigation/${page_id}`)
  }

  static fetchProgress(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/progress/`)
  }

}

export default ProjectsApi
