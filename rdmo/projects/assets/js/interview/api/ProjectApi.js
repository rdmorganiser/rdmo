import { isNil } from 'lodash'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ProjectsApi extends BaseApi {

  static fetchOverview(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/overview/`)
  }

  static fetchNavigation(projectId, page_id) {
    if (isNil(page_id)) {
      return this.get(`/api/v1/projects/projects/${projectId}/navigation/`)
    } else {
      return this.get(`/api/v1/projects/projects/${projectId}/navigation/${page_id}`)
    }
  }

  static fetchProgress(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/progress/`)
  }

  static fetchOptions(projectId, optionsetId) {
    return this.get(`/api/v1/projects/projects/${projectId}/options/${optionsetId}`)
  }

}

export default ProjectsApi
