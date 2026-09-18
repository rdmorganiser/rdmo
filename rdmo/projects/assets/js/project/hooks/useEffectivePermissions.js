import { useMemo } from 'react'
import { useSelector } from 'react-redux'

import { getEffectivePermissions } from '../../common/utils/permissions'

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
