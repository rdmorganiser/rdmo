import React from 'react'
import { useSelector } from 'react-redux'

import { Modal } from '../helper'
import { useModal }  from 'rdmo/core/assets/js/hooks'
import InviteMember from './InviteMember'

const Membership = () => {
  const { project } = useSelector((state) => state.project.project) ?? {}
  console.log('Project:', project)

  const { show, open, close } = useModal()

  const modalProps = {
    title: gettext('Invite member to project'),
    show,
    onClose: close
  }

  const membership = [
    ...(project?.authors ?? []).map(user => ({ ...user, role: gettext('author') })),
    ...(project?.guests ?? []).map(user => ({ ...user, role: gettext('guest') })),
    ...(project?.managers ?? []).map(user => ({ ...user, role: gettext('manager') })),
    ...(project?.owners ?? []).map(user => ({ ...user, role: gettext('owner') })),
  ]

  console.log('Membership:', membership)

  const renderHeader = () => (
    <div className="d-flex justify-content-between align-items-center mb-3">
      <h5 className="mb-0">{gettext('Membership')}</h5>
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


  return (
    <div>
      {renderHeader()}
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
          {membership.map((user, index) => (
            <tr key={index}>
              <td><strong>{user.full_name}</strong></td>
              <td>
                {user.email && <a href={`mailto:${user.email}`} className="link-success text-decoration-underline">{user.email}</a>}
              </td>
              <td>{user.role.charAt(0).toUpperCase() + user.role.slice(1)}</td>
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
      <Modal {...modalProps} size="modal-lg">
        <InviteMember />
      </Modal>
    </div>
  )
}

export default Membership
