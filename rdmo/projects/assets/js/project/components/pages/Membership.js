import React, { useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'

import { Modal } from '../helper'
import { useModal }  from 'rdmo/core/assets/js/hooks'
import Select from 'rdmo/core/assets/js/components/Select'
import { userIsManager } from 'rdmo/projects/assets/js/common/utils'
import { getFieldErrors } from '../../utils/getFieldErrors'
import InviteMember from './InviteMember'
import {
  addProjectMember,
  sendProjectInvite,
  deleteProjectMember,
  deleteProjectInvite,
  editProjectMember,
  editProjectInvite,
} from '../../actions/projectActions'

import { defaultRoleOptions as roleOptions } from '../../utils/defaultRoleOptions'

const Membership = () => {
  const dispatch = useDispatch()
  const [confirm, setConfirm] = useState(null)
  const { show, open, close } = useModal()
  const { show: showConfirm, open: openConfirm, close: closeConfirm } = useModal()

  const { memberships } = useSelector((state) => state.project.project) ?? {}
  const invites = useSelector((state) => state.project.invites)
  const currentUser = useSelector((state) => state.user.currentUser)

  const currentUserId = currentUser?.id

  const isManager = userIsManager(currentUser)
  const isOwner = memberships?.some(m => m.role === 'owner' && m.user === currentUserId)
  const isLastOwner = isOwner && memberships?.filter(m => m.role === 'owner').length === 1

  const compactSelectStyles = {
  control: (base) => ({
    ...base,
    minHeight: 28,
    height: 28,
    border: 0,
    boxShadow: 'none',
    backgroundColor: 'transparent'
    })
  }

  const compactComponents = {
    DropdownIndicator: null,
    IndicatorSeparator: null,
    ClearIndicator: null
  }

  const handleInviteSubmit = async (e) => {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)
    const silently = fd.has('silently')
    const payload = {
      lookup: (fd.get('lookup') || '').trim(),
      role: fd.get('role') || 'author'
    }

    try {
      await dispatch(silently ? addProjectMember(payload) : sendProjectInvite(payload))
      close()
    } catch (err) {
      // failure => keep modal open; InviteMember will show errors from state.project.errors
    }
  }

  const openDeleteConfirm = (person, isMember, isCurrentUser) => {
    const name =
      [person.first_name, person.last_name].filter(Boolean).join(' ').trim() ||
      person.email || ''

    setConfirm({
      title: isCurrentUser ? gettext('Leave project') : gettext('Remove person'),
      label: isCurrentUser ? gettext('Confirm leave') : gettext('Confirm delete'),
      body:  isCurrentUser
        ? gettext('Do you really want to leave this project?')
        : isMember ? interpolate(gettext('Do you really want to remove %s?'), [name])
        : interpolate(gettext('Do you really want to delete the invite for %s?'), [name]),
      onSubmit: () =>
        isMember
          ? dispatch(
              deleteProjectMember(
                person.id,
                isCurrentUser && !isManager
                  ? { redirect: true } // self-leave, redirect to projects list
                  : {}
              )
            )
          : dispatch(deleteProjectInvite(person.id))
    })
    openConfirm()
  }

  const modalProps = {
    title: gettext('Invite member to project'),
    show,
    onClose: close,
    onSubmit: () => {},
    submitLabel: gettext('Invite member'),
    submitProps: { type: 'submit', form: 'invite-member-form' }
  }

  const confirmModalProps = {
    title: confirm?.title || gettext('Confirm'),
    show: showConfirm,
    onClose: closeConfirm,
    onSubmit: async () => {
      try {
        await confirm?.onSubmit?.()
        closeConfirm()
      } catch {
        // keep Modal open on errors
      }
    },
    submitLabel: confirm?.label || gettext('Confirm'),
    submitProps: { className: 'btn btn-danger' }
  }

  const renderHeader = () => (
    <div className="d-flex justify-content-between align-items-center mb-3">
      <h5 className="mb-0">{gettext('Memberships')}</h5>
      { (isManager || isOwner) && (
        <button
          type="button"
          id="add-member"
          className="btn btn-link text-decoration-none"
          onClick={open}
        >
          <i className="bi bi-plus" aria-hidden="true"></i> {gettext('Add member')}
        </button>
      )}
    </div>
  )

  const renderTable = (people, isMember) => (
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
        {people?.map((person, index) => {
          const isCurrentUser = person.user === currentUserId
          const isUserOwner = isMember && isCurrentUser && person.role === 'owner'
          const showAction = ((!isOwner && isCurrentUser) || (isUserOwner && !isLastOwner) || (isOwner && !isUserOwner) || isManager)

          return (
            <tr key={index}>
              <td><strong>{person?.first_name} {person?.last_name}</strong></td>
              <td>
                {person.email && <a href={`mailto:${person.email}`} className="link-success text-decoration-underline">{person.email}</a>}
              </td>
              <td>
                <Select
                  options={roleOptions}
                  value={person.role}
                  onChange={(newRole) => {
                    if (!newRole) return
                    if (isMember) {
                      dispatch(editProjectMember(person.id, { role: newRole }))
                    } else {
                      dispatch(editProjectInvite(person.id, { role: newRole }))
                    }
                  }}
                  isClearable={false}
                  isDisabled={(!isOwner || isUserOwner) && !isManager}
                  styles={compactSelectStyles}
                  components={compactComponents}
                />
              </td>
              <td className="text-end">
                {showAction && (
                <button
                  type="button"
                  className="btn btn-link btn-sm p-0"
                  aria-label={isCurrentUser ? gettext('Leave') : gettext('Remove')}
                  title={isCurrentUser ? gettext('Leave') : gettext('Remove')}
                  onClick={() => openDeleteConfirm(person, isMember, isCurrentUser)}
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
  )

  return (
    <div>
      {renderHeader()}
      {memberships && renderTable(memberships, true)}
      {invites?.length > 0 && (
      <>
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="mb-0">{gettext('Invites')}</h5>
        </div>
        {invites && renderTable(invites, false)}
      </>
      )}
      <Modal {...modalProps} size="modal-lg">
        <form id="invite-member-form" key={show ? 'open' : 'closed'} onSubmit={handleInviteSubmit}>
          <InviteMember isManager={isManager} />
        </form>
      </Modal>
      <Modal {...confirmModalProps} size="modal-sm">
        <p className="mb-0">{confirm?.body || gettext('Are you sure?')}</p>
        {getFieldErrors('non_field_errors').map((err, i) => (
          <div key={i} className="text-danger mt-2">{err}</div>
        ))}
      </Modal>
    </div>
)}

export default Membership
