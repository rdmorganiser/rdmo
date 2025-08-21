import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import { defaultRoleOptions as roleOptions } from '../../utils/defaultRoleOptions'
import { getFieldErrors } from '../../utils/getFieldErrors'

const InviteMember = ({ isManager = false }) => {
  const templates = useSelector((state) => state.templates)

  return (
    <>
      <Html html={templates.project_view_invite_member} />

        {/* User */}
        <div className="mb-3">
          <label className="form-label fw-bold">{gettext('User')}</label>
          <input
            type="text"
            className="form-control mt-2"
            name="lookup"
            placeholder={gettext('Username or e-mail')}
            required
          />
          {getFieldErrors('lookup').map((err, i) => (
            <div key={i} className="text-danger mt-1">{err}</div>
          ))}
        </div>

        {/* Role */}
        <div className="mb-3">
          <label className="form-label fw-bold">{gettext('Role')}</label>

          {roleOptions.map(({ value, label }) => (
            <div className="form-check" key={value}>
              <input
                className="form-check-input"
                type="radio"
                id={`role-${value}`}
                name="role"
                value={value}
                defaultChecked={value === 'author'}
              />
              <label className="form-check-label" htmlFor={`role-${value}`}>
                {label}
              </label>
            </div>
          ))}
        {getFieldErrors('role').map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))}
        </div>

        {/* Add member silently */}
        { isManager && (
        <div className="mb-3">
          <label className="form-label fw-bold">{gettext('Add member silently')}</label>
          <Html html={templates.project_view_invite_member_silently_help}
          />
          <div className="form-check mt-1">
            <input className="form-check-input" type="checkbox" id="silently" name="silently" />
            <label className="form-check-label" htmlFor="silently">
              {gettext('Add member silently')}
            </label>
          </div>
        </div>
        )}
        {getFieldErrors('non_field_errors').map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))}
    </>
  )
}

InviteMember.propTypes = {
  isManager: PropTypes.bool
}

export default InviteMember
