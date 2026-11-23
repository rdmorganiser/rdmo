import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class RoleApi extends BaseApi {
  static fetchRoles() {
    return this.get('/api/v1/projects/roles/')
  }
}

export default RoleApi
