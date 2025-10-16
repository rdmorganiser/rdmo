import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { useModal }  from 'rdmo/core/assets/js/hooks'

import MembershipInviteModal from './MembershipInviteModal'
import MembershipTable from './MembershipTable'

const Membership = () => {
  const { show: showInvite, open: openInvite, close: closeInvite } = useModal()

  const { memberships, project } = useSelector((state) => state.project.project) ?? {}
  const { invites } = useSelector((state) => state.project)
  const perms = project?.permissions ?? {}

  return (
    <>
      <header className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">{gettext('Memberships')}</h5>
        {perms.can_add_invite && (
          <button
            type="button"
            id="add-member"
            className="btn btn-link text-decoration-none"
            onClick={openInvite}
          >
            <i className="bi bi-plus" aria-hidden="true"></i> {gettext('Add member')}
          </button>
        )}
      </header>
      {
        !isEmpty(memberships) && (
          <MembershipTable persons={memberships} type="memberships" />
        )
      }
      {
        !isEmpty(invites) && (
          <>
            <header className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">{gettext('Invites')}</h5>
            </header>
            <MembershipTable persons={invites} type="invites" />
          </>
        )
      }

      <MembershipInviteModal show={showInvite} onClose={closeInvite} />
    </>
  )
}

export default Membership
