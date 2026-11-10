import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { LinkButton } from 'rdmo/core/assets/js/components'
import { selectPermissions } from 'rdmo/projects/assets/js/common/selectors/permissions'

const ManagementButton = () => {
  const dispatch = useDispatch()
  const config = useSelector((state) => state.config)
  const perms = useSelector(selectPermissions)
  const text = config.showManagement ? gettext('Hide management panels') : gettext('Show management panels')

  const toggleManagement = () => {
    dispatch(updateConfig('showManagement', !config.showManagement))
  }

  return perms.can_view_management && (
    <div className="mb-2">
      <LinkButton title={text} onClick={toggleManagement}>
        <i className="bi bi-card-text me-1"></i> {text}
      </LinkButton>
    </div>
  )
}

export default ManagementButton
