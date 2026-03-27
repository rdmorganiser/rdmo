import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class RolesApi extends BaseApi {
  static fetchRoles() {
    return this.get('/api/v1/projects/roles/').then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error(response.statusText)
      }
    })
  }
}

export default RolesApi
