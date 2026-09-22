import { useMemo } from 'react'
import { useSelector } from 'react-redux'

import { combinePermissions } from '../../common/utils/permissions'

// return the combined model-based permissions for the current user and object-based permissions for the current project
export const usePermissions = () => {
  const projectPermissions = useSelector(
    (state) => state.project.project?.project?.permissions
  )
  const userPermissions = useSelector(
    (state) => state.user.currentUser?.permissions
  )

  return useMemo(
    () => combinePermissions(projectPermissions, userPermissions),
    [projectPermissions, userPermissions]
  )
}
