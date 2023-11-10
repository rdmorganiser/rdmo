import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ProjectsApi extends BaseApi {

  static fetchProjects() {
    console.log('fetch ')
    return this.get('/api/v1/projects/projects/')
  }
}

export default ProjectsApi
