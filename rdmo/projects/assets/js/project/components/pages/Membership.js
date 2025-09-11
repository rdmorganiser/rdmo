import React from 'react'
import { useSelector } from 'react-redux'

import { useModal }  from 'rdmo/core/assets/js/hooks'
import { userIsManager } from 'rdmo/projects/assets/js/common/utils'

import MembershipInviteModal from './MembershipInviteModal'
import MembershipTable from './MembershipTable'

const Membership = () => {
  const { show: showInvite, open: openInvite, close: closeInvite } = useModal()

  const { memberships } = useSelector((state) => state.project.project) ?? {}
  const invites = useSelector((state) => state.project.invites)
  const currentUser = useSelector((state) => state.user.currentUser)

  const currentUserId = currentUser?.id

  const isManager = userIsManager(currentUser)
  const isOwner = memberships?.some(m => m.role === 'owner' && m.user === currentUserId)

  return (
    <>
      <header className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">{gettext('Memberships')}</h5>
        {(isManager || isOwner) && (
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
      {memberships?.length > 0 && (
        <MembershipTable persons={memberships} isMember />
      )}
      {invites?.length > 0 && (
        <>
          <header className="d-flex justify-content-between align-items-center mb-3">
            <h5 className="mb-0">{gettext('Invites')}</h5>
          </header>
          <MembershipTable persons={invites} />
        </>
      )}

      <MembershipInviteModal show={showInvite} onClose={closeInvite} isManager={isManager} />
    </>
  )
}

export default Membership
