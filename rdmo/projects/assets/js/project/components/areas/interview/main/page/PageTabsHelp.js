import React from 'react'

import Template from 'rdmo/core/assets/js/components/Template'

import { usePermissions } from '../../../../../hooks'

const PageTabsHelp = () => {
  const perms = usePermissions()

  return (perms.can_add_value || perms.can_change_value || perms.can_delete_value) && (
    <div className="form-text">
      <Template template="project_interview_page_tabs_help" />
    </div>
  )
}

export default PageTabsHelp
