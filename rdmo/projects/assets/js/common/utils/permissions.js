// combine permission sets, granting a permission when it is true in any set
export const getEffectivePermissions = (...permissionSets) => {
  const effectivePermissions = {}

  permissionSets.forEach((permissions) => {
    Object.entries(permissions ?? {}).forEach(([key, value]) => {
      effectivePermissions[key] = effectivePermissions[key] === true || value === true
    })
  })

  return effectivePermissions
}
