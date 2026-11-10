import React from 'react'
import { useSelector } from 'react-redux'

import { selectPermissions } from 'rdmo/projects/assets/js/common/selectors/permissions'

import Template from 'rdmo/core/assets/js/components/Template'

const PageTabsHelp = () => {
  const perms = useSelector(selectPermissions)

  return (perms.can_add_value || perms.can_change_value || perms.can_delete_value) && (
    <div className="form-text">
      <Template template="project_interview_page_tabs_help" />
    </div>
  )
}

export default PageTabsHelp
