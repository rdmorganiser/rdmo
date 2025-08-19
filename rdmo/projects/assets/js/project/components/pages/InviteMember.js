import React from 'react'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

const InviteMember = () => {
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
        </div>

        {/* Role */}
        <div className="mb-3">
          <label className="form-label fw-bold">{gettext('Role')}</label>

          <div className="form-check">
            <input className="form-check-input" type="radio" id="role-owner" name="role" value="owner" />
            <label className="form-check-label" htmlFor="role-owner">{gettext('Owner')}</label>
          </div>
          <div className="form-check">
            <input className="form-check-input" type="radio" id="role-manager" name="role" value="manager" />
            <label className="form-check-label" htmlFor="role-manager">{gettext('Manager')}</label>
          </div>
          <div className="form-check">
            <input className="form-check-input" type="radio" id="role-author" name="role" value="author" defaultChecked />
            <label className="form-check-label" htmlFor="role-author">{gettext('Author')}</label>
          </div>
          <div className="form-check">
            <input className="form-check-input" type="radio" id="role-guest" name="role" value="guest" />
            <label className="form-check-label" htmlFor="role-guest">{gettext('Guest')}</label>
          </div>
        </div>

        {/* Add member silently */}
        {/* TODO: conditional rendering based on user role */}
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
    </>
  )
}

export default InviteMember
