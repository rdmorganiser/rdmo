import { useMemo } from 'react'
import { useSelector } from 'react-redux'

import { getEffectivePermissions } from '../../common/utils/permissions'

// return the combined model-based permissions for the current user and object-based permissions for the current project
export const useEffectivePermissions = () => {
  const projectPermissions = useSelector(
    (state) => state.project.project?.project?.permissions
  )
  const userPermissions = useSelector(
    (state) => state.user.currentUser?.permissions
  )

  return useMemo(
    () => getEffectivePermissions(projectPermissions, userPermissions),
    [projectPermissions, userPermissions]
  )
}
