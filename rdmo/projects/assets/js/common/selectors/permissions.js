import { createSelector } from '@reduxjs/toolkit'

import { combinePermissions, isReadOnly } from '../utils/permissions'

export const selectPermissions = createSelector(
  [
    (state) => state.project.project?.permissions,
    (state) => state.user.currentUser?.permissions
  ],
  combinePermissions
)

export const selectReadOnly = (state) => isReadOnly(selectPermissions(state))
