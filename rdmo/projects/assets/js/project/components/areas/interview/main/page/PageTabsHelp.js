import React from 'react'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { usePermissions } from '../../../../../hooks'

const PageTabsHelp = () => {
  const templates = useSelector((state) => state.templates)
  const perms = usePermissions()

  return (perms.can_add_value || perms.can_change_value || perms.can_delete_value) && (
    <div className="form-text">
      <Html html={templates.project_interview_page_tabs_help} />
    </div>
  )
}

export default PageTabsHelp
