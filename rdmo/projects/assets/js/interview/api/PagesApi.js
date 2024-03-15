import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ProjectsApi extends BaseApi {

  static fetchPage(projectId, page_id) {
    return this.get(`/api/v1/projects/projects/${projectId}/pages/${page_id}`)
  }

  static fetchContinue(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/pages/continue/`)
  }

}

export default ProjectsApi
