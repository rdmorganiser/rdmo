import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useSelector, useDispatch } from 'react-redux'
import classNames from 'classnames'

import { useModal } from 'rdmo/core/assets/js/hooks'

import Select from 'rdmo/core/assets/js/components/Select'

import { updateProjectMember, updateProjectInvite } from '../../../actions/projectActions'

import MembershipDeleteModal from './MembershipDeleteModal'

const MembershipTable = ({ persons, type }) => {
  const dispatch = useDispatch()
  const currentUser = useSelector((state) => state.user.currentUser)
  const { project } = useSelector((state) => state.project.project) || {}
  const perms = project?.permissions || {}
  const roleOptions = useSelector((state) => state.roles?.roles) || []
  const { show: showConfirm, open: openConfirm, close: closeConfirm } = useModal()
  const [modalState, setModalState] = useState(null)

  const isAdminOrSiteManager = currentUser?.is_superuser || currentUser?.is_site_manager

  const openDeleteModal = (person, isCurrentUser) => {
    setModalState({ person, isCurrentUser })
    openConfirm()
  }

  const closeDeleteModal = () => {
    setModalState(null)
    closeConfirm()
  }

  const uniquePersons = (type === 'memberships') ? persons.filter(
    (p, i, arr) => arr.findIndex(x => x.user?.id === p.user?.id) === i
  ) : persons

  return (
    <div>
      <table className="table align-middle">
        <thead>
          <tr>
            <th style={{ width: '35%' }}>{gettext('Name')}</th>
            <th style={{ width: '40%' }}>{gettext('Email')}</th>
            <th style={{ width: '20%' }}>{gettext('Role')}</th>
            <th style={{ width: '5%' }}></th>
          </tr>
        </thead>
        <tbody>
          {uniquePersons?.map((person, index) => {
            const isCurrentUser = person.user?.id === currentUser?.id
            const isOwner = isCurrentUser && person.role == 'owner'

            const showMemberAction = (type === 'memberships') && (
              isCurrentUser ? perms.can_leave_project : perms.can_delete_membership
            )
            const showInviteAction = (type === 'invites') && perms.can_delete_invite
            const showActions = (
              showMemberAction || showInviteAction || isAdminOrSiteManager
            ) && !person.project // do not show action buttons for hierarchy roles

            const emailAddress = person.user?.email || person?.email
            const hierarchyRole = person?.project ? interpolate(gettext('%s of %s'), [
              roleOptions.find(opt => opt.value === person.role)?.label || '',
              person.project.title
            ]) : null

            return (
              <tr key={index}>
                <td><strong>{person?.user?.first_name} {person?.user?.last_name}</strong></td>
                <td>
                  {
                    emailAddress && (
                      <a href={`mailto:${emailAddress}`} className="link-success text-decoration-underline">
                        {emailAddress}
                      </a>
                    )
                  }
                </td>
                <td>
                  {hierarchyRole ?
                    <div className="mb-1">{hierarchyRole}</div>
                    :
                    <Select
                      options={roleOptions}
                      value={person.role}
                      onChange={(newRole) => {
                        if (!newRole) return
                        (type === 'memberships') ? dispatch(updateProjectMember(person.id, { role: newRole }))
                          : dispatch(updateProjectInvite(person.id, { role: newRole }))
                      }}
                      isClearable={false}
                      isDisabled={(
                        (type === 'memberships') ? (
                          !perms.can_change_membership || (isOwner && !isAdminOrSiteManager)
                        ) : !perms.can_change_invite
                      )}
                    />
                  }
                </td>
                <td className="text-end">
                  {showActions && (
                    <button type="button" className="btn link"
                      aria-label={isCurrentUser ? gettext('Leave') : gettext('Remove')}
                      title={isCurrentUser ? gettext('Leave') : gettext('Remove')}
                      onClick={() => openDeleteModal(person, isCurrentUser)}
                    >
                      <i
                        className={classNames('bi', isCurrentUser ? 'bi-box-arrow-right' : 'bi-person-x')}
                        aria-hidden="true"
                      />
                    </button>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
      {
        modalState && (
          <MembershipDeleteModal
            type={type}
            show={showConfirm}
            person={modalState.person}
            onClose={closeDeleteModal}
            isAdminOrSiteManager={isAdminOrSiteManager}
            isCurrentUser={modalState.isCurrentUser}
          />
        )
      }
    </div>
  )
}

MembershipTable.propTypes = {
  persons: PropTypes.array.isRequired,
  type: PropTypes.oneOf(['memberships', 'invites'])
}

export default MembershipTable
