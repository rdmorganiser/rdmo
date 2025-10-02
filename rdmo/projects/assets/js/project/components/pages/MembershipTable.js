import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useSelector, useDispatch } from 'react-redux'

import { useModal } from 'rdmo/core/assets/js/hooks'

import Select from 'rdmo/core/assets/js/components/Select'

import { updateProjectMember, updateProjectInvite } from '../../actions/projectActions'
import { defaultRoleOptions as roleOptions } from '../../../common/constants/defaultRoleOptions'

import MembershipDeleteModal  from './MembershipDeleteModal'

const MembershipTable = ({ persons, isMember = false }) => {
  const dispatch = useDispatch()
  const currentUser = useSelector((state) => state.user.currentUser)
  const { perms } = useSelector((state) => state.project)

  const { show: showConfirm, open: openConfirm, close: closeConfirm } = useModal()
  const [selected, setSelected] = useState(null)

  const currentUserId = currentUser?.id
  const isAdmin = currentUser?.is_superuser || currentUser?.is_site_manager

  const handleOpenConfirm = (person, isCurrentUser) => {
    setSelected({ person, isCurrentUser })
    openConfirm()
  }

  const handleCloseConfirm = () => {
    setSelected(null)
    closeConfirm()
  }

  const uniquePersons = isMember
  ? persons.filter(
      (p, i, arr) => arr.findIndex(x => x.user?.id === p.user?.id) === i
    )
  : persons

  return (
    <div>
      <table className="table border align-middle">
        <thead className="table-light">
          <tr>
            <th style={{ width: '35%' }}>{gettext('Name').toUpperCase()}</th>
            <th style={{ width: '40%' }}>{gettext('Email').toUpperCase()}</th>
            <th style={{ width: '20%' }}>{gettext('Role').toUpperCase()}</th>
            <th style={{ width: '5%' }}></th>
          </tr>
        </thead>
        <tbody>
          {uniquePersons?.map((person, index) => {
            const isCurrentUser = person.user?.id === currentUserId
            const isOwner = isCurrentUser && person.role == 'owner'
            const showMemberAction = isMember && ((!isCurrentUser && perms.can_delete_membership) || (isCurrentUser && perms.can_leave_project))
            const showInviteAction = !isMember && perms.can_delete_invite
            const showAction = (showMemberAction || showInviteAction || isAdmin) && !person.project // do not show action buttons for hierarchy roles

            const emailAddress = person.user?.email || person?.email
            const hierarchyRole = person?.project
                      ? `${roleOptions.find(opt => opt.value === person.role).label} ${gettext('of')} ${person.project.title}`
                      : null

            return (
              <tr key={index}>
                <td><strong>{person?.user?.first_name} {person?.user?.last_name}</strong></td>
                <td>
                  {emailAddress && <a href={`mailto:${emailAddress}`} className="link-success text-decoration-underline">{emailAddress}</a>}
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
                        if (isMember) {
                          dispatch(updateProjectMember(person.id, { role: newRole }))
                        } else {
                          dispatch(updateProjectInvite(person.id, { role: newRole }))
                        }
                      }}
                      isClearable={false}
                      isDisabled={(isMember && (!perms.can_change_membership || (isOwner && !isAdmin)) || (!isMember && !perms.can_change_invite))}
                    />
                }
                </td>
                <td className="text-end">
                  {showAction && (
                    <button
                      type="button"
                      className="btn btn-link btn-sm p-0"
                      aria-label={isCurrentUser ? gettext('Leave') : gettext('Remove')}
                      title={isCurrentUser ? gettext('Leave') : gettext('Remove')}
                      onClick={() => handleOpenConfirm(person, isCurrentUser)}
                    >
                      <i
                        className={`bi ${isCurrentUser ? 'bi-box-arrow-right' : 'bi-x'}`}
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
      {selected && (
        <MembershipDeleteModal
          show={showConfirm}
          onClose={handleCloseConfirm}
          isAdmin={isAdmin}
          isMember={isMember}
          isCurrentUser={selected.isCurrentUser}
          person={selected.person}
        />
      )}
    </div>
  )
}

MembershipTable.propTypes = {
  persons: PropTypes.array.isRequired,
  isMember: PropTypes.bool
}

export default MembershipTable
