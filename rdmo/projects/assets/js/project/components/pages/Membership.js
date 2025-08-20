import React, { useRef } from 'react'
import { useSelector, useDispatch } from 'react-redux'

import { Modal } from '../helper'
import { useModal }  from 'rdmo/core/assets/js/hooks'
import InviteMember from './InviteMember'
import EditRole from './EditRole'
import { addProjectMember, sendProjectInvite, deleteProjectMember, deleteProjectInvite, editProjectMember, editProjectInvite } from '../../actions/projectActions'

const Membership = () => {
  const { project, memberships } = useSelector((state) => state.project.project) ?? {}
  const invites = useSelector((state) => state.project.invites)

  console.log('Project:', project)
  console.log('Invites:', invites)
  console.log('Memberships:', memberships)

  const { show, open, close } = useModal()
  const { show: showEdit, open: openEdit, close: closeEdit } = useModal()

  const editRowRef = useRef(null)
  const editSubmitRef = useRef(null)

  const dispatch = useDispatch()

  const handleInviteSubmit = (e) => {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)

    const silently = fd.get('silently') === 'on'
    const payload = {
      lookup: (fd.get('lookup') || '').trim(),
      role: fd.get('role') || 'author',
    }

    if (silently) {
      dispatch(addProjectMember(payload))
    } else {
      dispatch(sendProjectInvite(payload))
    }

    close()
  }

  const handleRoleEdit = (e) => {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)
    const role = fd.get('role') // || editRowRef.current?.role
    if (editSubmitRef.current) {
      editSubmitRef.current(role)
    }
    closeEdit()
  }

  const handleDeleteMember = (member) => {
  dispatch(deleteProjectMember(member.id))
  }

  const handleDeleteInvite = (invite) => {
    dispatch(deleteProjectInvite(invite.id))
  }

  const handleEditMember = (member) => {
    dispatch(editProjectMember(member.id, { role: member.role }))
  }

  const handleEditInvite = (invite) => {
    dispatch(editProjectInvite(invite.id, { role: invite.role }))
  }

  const modalProps = {
    title: gettext('Invite member to project'),
    show,
    onClose: close,
    onSubmit: () => {},
    submitLabel: gettext('Invite member'),
    submitProps: { type: 'submit', form: 'invite-member-form' }
  }

    const editModalProps = {
    title: gettext('Invite member to project'),
    show: showEdit,
    onClose: closeEdit,
    onSubmit: () => {},
    submitLabel: gettext('Change role'),
    submitProps: { type: 'submit', form: 'change-role-form' }
  }

  const renderHeader = () => (
    <div className="d-flex justify-content-between align-items-center mb-3">
      <h5 className="mb-0">{gettext('Memberships')}</h5>
      {/* TODO: conditional rendering of button based on user role */}
      <button
        type="button"
        id="add-member"
        className="btn btn-link text-decoration-none"
        onClick={open}
      >
        <i className="bi bi-plus" aria-hidden="true"></i> {gettext('Add member')}
      </button>
    </div>
  )

  const renderTable = (people, onDelete, isMember) => (
    <table className="table border align-middle">
      <thead className="table-light">
        <tr>
          <th style={{ width: '35%' }}>{gettext('Name').toUpperCase()}</th>
          <th style={{ width: '45%' }}>{gettext('Email').toUpperCase()}</th>
          <th style={{ width: '15%' }}>{gettext('Role').toUpperCase()}</th>
          <th style={{ width: '5%' }}></th>
        </tr>
      </thead>
      <tbody>
        {people?.map((person, index) => (
          <tr key={index}>
            <td><strong>{person?.first_name} {person?.last_name}</strong></td>
            <td>
              {person.email && <a href={`mailto:${person.email}`} className="link-success text-decoration-underline">{person.email}</a>}
            </td>
            <td>{person.role.charAt(0).toUpperCase() + person.role.slice(1)}</td>
            {/* TODO: add permission based logic for dropdown actions */}
            <td className="text-end">
              {/* <div className="dropdown project-dropdown" tabIndex={-1}> */}
              <div
                className="dropdown project-dropdown dropstart"
                tabIndex={-1}
                onMouseLeave={(e) => {
                  const focused = e.currentTarget.querySelector(':focus')
                  focused?.blur()
                }}
              >
                <button className="btn btn-sm btn-link" type="button" aria-expanded="false">
                  <i className="bi bi-three-dots" />
                </button>
                {/* <ul className="dropdown-menu dropdown-menu-end"> */}
                <ul className="dropdown-menu">
                  <li>
                    {/* <a className="dropdown-item" href="#">{gettext('Edit')}</a> */}
                    <a
                      className="dropdown-item"
                      href="#"
                      onClick={() => {
                        editRowRef.current = person
                        editSubmitRef.current = (newRole) => {
                          if (isMember) {
                            handleEditMember({ id: person.id, role: newRole })
                          } else {
                            handleEditInvite({ id: person.id, role: newRole })
                          }
                        }
                        openEdit()
                      }}
                    >
                      {gettext('Edit')}
                    </a>
                  </li>
                  <li>
                    {/* <a className="dropdown-item" href="#">{gettext('Remove')}</a> */}
                    <button
                      type="button"
                      className="dropdown-item"
                      onClick={(e) => {
                        onDelete?.(person)
                        e.currentTarget.closest('.project-dropdown')?.querySelector(':focus')?.blur()
                      }}
                    >
                      {gettext('Remove')}
                    </button>
                    {/* <a
                      className="dropdown-item"
                      href="#"
                      onClick={(e) => {
                        e.preventDefault()
                        onDelete?.(person)
                      }}
                    >
                      {gettext('Remove')}
                    </a> */}
                  </li>
                </ul>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )

  return (
    <div>
      {renderHeader()}
      {memberships && renderTable(memberships, handleDeleteMember, true)}
      {invites?.length > 0 && (
      <>
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="mb-0">{gettext('Invites')}</h5>
        </div>
        {invites && renderTable(invites, handleDeleteInvite, false)}
      </>
      )}
      <Modal {...modalProps} size="modal-lg">
        <form id="invite-member-form" key={show ? 'open' : 'closed'} onSubmit={handleInviteSubmit}>
          <InviteMember />
        </form>
      </Modal>
      <Modal {...editModalProps} size="modal-lg">
        <form id="change-role-form" key={showEdit ? 'open' : 'closed'} onSubmit={handleRoleEdit}>
          <EditRole row={editRowRef.current} />
        </form>
      </Modal>
    </div>
)}

export default Membership
