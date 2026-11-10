import React from 'react'

import Template from 'rdmo/core/assets/js/components/Template'

import { usePermissions } from '../../../../../hooks'

const PageAddTabHelp = () => {
  const perms = usePermissions()

  return (perms.can_add_value || perms.can_change_value || perms.can_delete_value) && (
    <Template template="project_interview_page_add_tab_help" />
  )
}

export default PageAddTabHelp
