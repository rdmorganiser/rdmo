import React from 'react'
import { useSelector, useDispatch } from 'react-redux'

import { Modal } from '../helper'
import { useModal }  from 'rdmo/core/assets/js/hooks'
import InviteMember from './InviteMember'
import { addProjectMember, sendProjectInvite } from '../../actions/projectActions'

const Membership = () => {
  const { project, memberships } = useSelector((state) => state.project.project) ?? {}
  const invites = useSelector((state) => state.project.invites)

  console.log('Project:', project)
  console.log('Invites:', invites)
  console.log('Memberships:', memberships)

  const { show, open, close } = useModal()
  const dispatch = useDispatch()

  // const submitWithMail = (payload) => dispatch(sendProjectInvite(payload))
  // const submitSilently = (payload) => dispatch(addProjectMember(payload))

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

  const modalProps = {
    title: gettext('Invite member to project'),
    show,
    onClose: close,
    onSubmit: () => {},
    submitLabel: gettext('Invite member'),
    submitProps: { type: 'submit', form: 'invite-member-form' }
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

  const renderTable = (people) => (
    <table className="table border align-middle">
      <thead className="table-light">
        <tr>
          <th scope="col">{gettext('Name').toUpperCase()}</th>
          <th scope="col">{gettext('Email').toUpperCase()}</th>
          <th scope="col">{gettext('Role').toUpperCase()}</th>
          <th scope="col"></th>
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
            <td className="text-end">
              <div className="dropdown">
                <button
                  className="btn btn-sm btn-link"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <i className="bi bi-three-dots"></i>
                </button>
                <ul className="dropdown-menu dropdown-menu-end">
                  <li><a className="dropdown-item" href="#">Edit</a></li>
                  <li><a className="dropdown-item" href="#">Remove</a></li>
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
      {memberships && renderTable(memberships)}
      {invites?.length > 0 && (
      <>
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="mb-0">{gettext('Invites')}</h5>
        </div>
        {invites && renderTable(invites)}
      </>
      )}
      <Modal {...modalProps} size="modal-lg">
        <form id="invite-member-form" key={show ? 'open' : 'closed'} onSubmit={handleInviteSubmit}>
          <InviteMember />
        </form>
      </Modal>
    </div>
)}

export default Membership
