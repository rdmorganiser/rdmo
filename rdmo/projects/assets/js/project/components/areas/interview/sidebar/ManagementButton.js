import React from 'react'
import { useSelector } from 'react-redux'

import { LinkButton } from 'rdmo/core/assets/js/components'
import { useConfig } from 'rdmo/core/assets/js/hooks'
import { selectPermissions } from 'rdmo/projects/assets/js/common/selectors/permissions'

const ManagementButton = () => {
  const [showManagement, setShowManagement] = useConfig('showManagement', false)
  const perms = useSelector(selectPermissions)
  const text = showManagement ? gettext('Hide management panels') : gettext('Show management panels')

  const toggleManagement = () => setShowManagement(!showManagement)

  return perms.can_view_management && (
    <div className="mb-2">
      <LinkButton title={text} onClick={toggleManagement}>
        <i className="bi bi-card-text me-1"></i> {text}
      </LinkButton>
    </div>
  )
}

export default ManagementButton
