import BaseApi from 'rdmo/core/assets/js/api/BaseApi'

class AccountsApi extends BaseApi {
  static fetchCurrentUser() {
    return this.get('/api/v1/accounts/users/current/')
  }
}

export default AccountsApi
