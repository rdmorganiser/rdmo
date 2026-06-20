import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

const PendingInvitations = ({ invitations }) => {
  const roleOptions = useSelector((state) => state.roles?.roles) || []

  return invitations?.map((item) => {
    const roleLabel = roleOptions.find(
      (option) => option.value === item.role
    )?.label

    return (
      <div key={item.id} className="row g-2 align-items-center">
        <div className="mb-1">
          <b>{item.title}</b>
        </div>

        <div className="d-flex gap-2">
          <div className="me-auto">
            {roleLabel && interpolate(gettext('Role: %s'), [roleLabel])}
          </div>

          <button
            type="button"
            className="btn btn-sm btn-success"
            onClick={
              () => {
                window.location.href = `${baseUrl}/projects/join/${item.token}/`
              }
            }
          >
            {gettext('Accept')}
          </button>

          <button
            type="button"
            className="btn btn-sm btn-danger"
            onClick={
              () => {
                window.location.href = `${baseUrl}/projects/cancel/${item.token}/`
              }
            }
          >
            {gettext('Decline')}
          </button>
        </div>
      </div>
    )
  })
}

PendingInvitations.propTypes = {
  invitations: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
    project: PropTypes.number.isRequired,
    role: PropTypes.string.isRequired,
    token: PropTypes.string.isRequired
  })),
}

export default PendingInvitations
