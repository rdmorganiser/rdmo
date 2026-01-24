import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { useModal } from 'rdmo/core/assets/js/hooks'

import MembershipInviteModal from './memberships/MembershipInviteModal'
import MembershipTable from './memberships/MembershipTable'

const Memberships = () => {
  const { show: showInvite, open: openInvite, close: closeInvite } = useModal()

  const { memberships, project } = useSelector((state) => state.project.project) ?? {}
  const { invites } = useSelector((state) => state.project)
  const perms = project?.permissions ?? {}

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-5">
        <h1 className="mb-0">{gettext('Memberships')}</h1>
        {perms.can_add_invite && (
          <button type="button" className="btn link small" onClick={openInvite}>
            <i className="bi bi-plus" aria-hidden="true"></i> {gettext('Add member')}
          </button>
        )}
      </div>
      {
        !isEmpty(memberships) && (
          <MembershipTable persons={memberships} type="memberships" />
        )
      }
      {
        !isEmpty(invites) && (
          <>
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h2 className="mb-0">{gettext('Invites')}</h2>
            </div>
            <MembershipTable persons={invites} type="invites" />
          </>
        )
      }

      <MembershipInviteModal show={showInvite} onClose={closeInvite} />
    </>
  )
}

export default Memberships
