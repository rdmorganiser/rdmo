import React from 'react'

import { LinkButton } from 'rdmo/core/assets/js/components'
import { useConfigToggle } from 'rdmo/core/assets/js/hooks'

import { usePermissions } from '../../../../hooks'

const ManagementButton = () => {
  const [showManagement, toggleShowManagement] = useConfigToggle('showManagement')
  const perms = usePermissions()
  const text = showManagement ? gettext('Hide management panels') : gettext('Show management panels')


  return perms.can_view_management && (
    <div className="mb-2">
      <LinkButton title={text} onClick={toggleShowManagement}>
        <i className="bi bi-card-text me-1"></i> {text}
      </LinkButton>
    </div>
  )
}

export default ManagementButton
