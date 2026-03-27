import RoleApi from '../api/RoleApi'

import { FETCH_ROLES_INIT, FETCH_ROLES_ERROR, FETCH_ROLES_SUCCESS } from './actionTypes'

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
  return { type: FETCH_ROLES_INIT }
}

export function fetchRolesSuccess(roles) {
  return { type: FETCH_ROLES_SUCCESS, roles }
}

export function fetchRolesError(errors) {
  return { type: FETCH_ROLES_ERROR, errors }
}
