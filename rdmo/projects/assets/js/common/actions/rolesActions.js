import { serializeError } from 'rdmo/core/assets/js/utils/errors'

import { actions } from '../reducers/rolesSlice'

import RoleApi from '../api/RoleApi'

export function fetchRoles() {
  return function (dispatch) {
    dispatch(fetchRolesInit())

    return RoleApi.fetchRoles()
      .then((roles) => {
        const mappedRoles = roles.map(role => ({
          value: role.id,
          label: role.text,
        }))
        dispatch(fetchRolesSuccess(mappedRoles))
      })
      .catch((errors) => dispatch(fetchRolesError(errors)))
  }
}

export function fetchRolesInit() {
  return actions.fetchRolesInit()
}

export function fetchRolesSuccess(roles) {
  return actions.fetchRolesSuccess(roles)
}

export function fetchRolesError(errors) {
  return actions.fetchRolesError(serializeError(errors))
}
