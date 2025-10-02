import { defaultRoleOptions as roleOptions, defaultRoleArrays as roleArrays } from '../../common/constants/defaultRoleOptions'

export const getUserRole = (project, currentUserId) => {
  let roleLabel = null
  roleArrays.forEach(arrayName => {
    if (project[arrayName].some(item => item.id === currentUserId)) {
      roleLabel = roleOptions.find(opt => opt.value === arrayName.slice(0, -1)).label
    }
  })

  return roleLabel
}

export default getUserRole
