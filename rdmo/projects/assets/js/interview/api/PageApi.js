import { isNil } from 'lodash'

import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class ProjectsApi extends BaseApi {

  static fetchPage(projectId, pageId, back) {
    if (isNil(back)) {
      return this.get(`/api/v1/projects/projects/${projectId}/pages/${pageId}/`)
    } else {
      return this.get(`/api/v1/projects/projects/${projectId}/pages/${pageId}/?back=true`)
    }
  }

  static fetchContinue(projectId) {
    return this.get(`/api/v1/projects/projects/${projectId}/pages/continue/`)
  }

}

export default ProjectsApi
