// rdmo/projects/assets/js/project/components/pages/EditRow.jsx
import React from 'react'
import PropTypes from 'prop-types'

const EditRow = ({ row }) => {
  if (!row) return null

  const fullName =
    [row.first_name, row.last_name].filter(Boolean).join(' ').trim() || row.email

  const currentRole = row.role // || 'author'

  return (
    <>
      <p className="mb-3">
        {gettext('Change role for')} <strong>{fullName}</strong>
      </p>

      <div className="mb-3">
        <label className="form-label fw-bold">{gettext('Role')}</label>

        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            id="edit-role-owner"
            name="role"
            value="owner"
            defaultChecked={currentRole === 'owner'}
          />
          <label className="form-check-label" htmlFor="edit-role-owner">
            {gettext('Owner')}
          </label>
        </div>

        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            id="edit-role-manager"
            name="role"
            value="manager"
            defaultChecked={currentRole === 'manager'}
          />
        <label className="form-check-label" htmlFor="edit-role-manager">
            {gettext('Manager')}
          </label>
        </div>

        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            id="edit-role-author"
            name="role"
            value="author"
            defaultChecked={currentRole === 'author'}
          />
          <label className="form-check-label" htmlFor="edit-role-author">
            {gettext('Author')}
          </label>
        </div>

        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            id="edit-role-guest"
            name="role"
            value="guest"
            defaultChecked={currentRole === 'guest'}
          />
          <label className="form-check-label" htmlFor="edit-role-guest">
            {gettext('Guest')}
          </label>
        </div>
      </div>
    </>
  )
}

EditRow.propTypes = {
  row: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    first_name: PropTypes.string,
    last_name: PropTypes.string,
    email: PropTypes.string,
    role: PropTypes.oneOf(['owner', 'manager', 'author', 'guest'])
  }).isRequired
}

export default EditRow
