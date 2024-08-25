import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

export default class ProjectsApi extends BaseApi {

  static fetchProject(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/overview/`)
  }

}
