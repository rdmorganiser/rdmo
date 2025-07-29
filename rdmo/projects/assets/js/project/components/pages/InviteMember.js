import React from 'react'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import { projectId }  from '../../utils/meta'

const InviteMember = () => {
  console.log('Project ID:', projectId)
  const templates = useSelector((state) => state.templates)
  console.log('templates %o', templates)
  return (
    <>
      <Html html={templates.project_view_invite_member} />
    </>
  )
}


export default InviteMember
