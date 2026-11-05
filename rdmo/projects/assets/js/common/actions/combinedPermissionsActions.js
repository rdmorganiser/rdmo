import { actions } from '../reducers/combinedPermissionsSlice'
import { combinePermissions } from '../utils/permissions'

export function updateCombinedPermissions(...permissionSets) {
  return actions.updateCombinedPermissions(combinePermissions(...permissionSets))
}
