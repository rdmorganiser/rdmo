import { isNil } from 'lodash'

import { encodeParams } from 'rdmo/core/assets/js/utils/api'

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

  static updateProgress(projectId) {
    return this.post(`/api/v1/projects/projects/${projectId}/progress/`)
  }

  static fetchOptions(projectId, optionsetId) {
    return this.get(`/api/v1/projects/projects/${projectId}/options/?${encodeParams({ optionset: optionsetId })}`)
  }

}

export default ProjectsApi
