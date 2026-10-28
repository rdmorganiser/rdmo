// combine permission sets, granting a permission when it is true in any set
export const combinePermissions = (...permissionSets) => {
  const effectivePermissions = {}

  permissionSets.forEach((permissions) => {
    Object.entries(permissions ?? {}).forEach(([key, value]) => {
      effectivePermissions[key] = effectivePermissions[key] === true || value === true
    })
  })

  return effectivePermissions
}

// the interview is read-only unless values can be added, changed and deleted
export const isReadOnly = (permissions) => (
  !(permissions.can_add_value && permissions.can_change_value && permissions.can_delete_value)
)
