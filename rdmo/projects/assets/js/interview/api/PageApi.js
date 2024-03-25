import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ProjectsApi extends BaseApi {

  static fetchPage(projectId, pageId) {
    return this.get(`/api/v1/projects/projects/${projectId}/pages/${pageId}`)
  }

  static fetchContinue(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/pages/continue/`)
  }

}

export default ProjectsApi
