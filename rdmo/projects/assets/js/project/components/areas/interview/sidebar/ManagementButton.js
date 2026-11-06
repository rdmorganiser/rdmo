import React from 'react'
import { useSelector } from 'react-redux'

import { LinkButton } from 'rdmo/core/assets/js/components'
import { useConfigToggle } from 'rdmo/core/assets/js/hooks'
import { selectPermissions } from 'rdmo/projects/assets/js/common/selectors/permissions'

const ManagementButton = () => {
  const [showManagement, toggleShowManagement] = useConfigToggle('showManagement')
  const perms = useSelector(selectPermissions)
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
