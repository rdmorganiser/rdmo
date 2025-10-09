import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import { Modal, Tooltip } from 'rdmo/core/assets/js/_bs53/components'

import { createProjectMember, sendProjectInvite, clearProjectErrors } from '../../actions/projectActions'
import { useFieldErrors } from '../../hooks/useFieldErrors'
import { roleOptions } from '../../../common/constants/roles'

const initialForm = { lookup: '', role: 'author' }

const MembershipInviteModal = ({ show, onClose }) => {
  const dispatch = useDispatch()
  const templates = useSelector((state) => state.templates)
  const { project } = useSelector((state) => state.project.project) || {}
  const errors = useFieldErrors()
  const perms = project?.permissions || {}

  const [formData, setFormData] = useState(initialForm)
  const [silently, setSilently] = useState(false)

  useEffect(() => {
    if (show) {
      setFormData(initialForm)
      setSilently(false)
      dispatch(clearProjectErrors())
    }
  }, [show])

  const setField = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await dispatch(silently ? createProjectMember(formData) : sendProjectInvite(formData))
      onClose()
    } catch {
      // keep modal open; errors are shown via useFieldErrors
    }
  }

  return (
    <Modal
      title={gettext('Invite member to project')}
      show={show}
      onClose={onClose}
      onSubmit={() => {}} // render the Modal's submit button
      submitLabel={gettext('Invite member')}
      submitProps={{ type: 'submit', form: 'invite-member-form' }}
      size="modal-lg"
    >
      <form id="invite-member-form" onSubmit={handleSubmit}>
        <Html html={templates.project_view_invite_member} />
        {/* User */}
        <div className="mb-3">
          <label className="form-label fw-bold" htmlFor="invite-lookup">
            {gettext('User')}
          </label>
          <input
            id="invite-lookup"
            type="text"
            className="form-control mt-2"
            name="lookup"
            placeholder={gettext('Username or e-mail')}
            required
            value={formData.lookup}
            onChange={(e) => setField('lookup', e.target.value)}
          />
          {errors.lookup?.map((err, i) => (
            <div key={i} className="text-danger mt-1">{err}</div>
          ))}
        </div>
        {/* Role */}
        <div className="mb-3">
          <label className="form-label fw-bold">{gettext('Role')}</label>
          {roleOptions.map(({ value, label }) => (
            <div className="form-check d-flex align-items-center" key={value}>
              <input
                className="form-check-input"
                type="radio"
                id={`role-${value}`}
                name="role"
                value={value}
                checked={formData.role === value}
                onChange={() => setField('role', value)}
              />
              <label className="form-check-label ms-2" htmlFor={`role-${value}`}>
                {label}
              </label>
              <Tooltip
                title={
                  <Html
                    html={templates[`project_view_${value}_info`]}
                  />
                }
                placement="right"
              >
                <i
                  className="bi bi-info-circle ms-2"
                  tabIndex={0}
                  role="img"
                  aria-label={gettext('Role information')}
                  style={{ cursor: 'pointer' }}
                />
              </Tooltip>
            </div>
          ))}
          {errors.role?.map((err, i) => (
            <div key={i} className="text-danger mt-1">{err}</div>
          ))}
        </div>
        {/* Add member silently */}
        {perms.can_add_membership && (
          <div className="mb-3">
            <label className="form-label fw-bold">{gettext('Add member silently')}</label>
            <Html html={templates.project_view_invite_member_silently_help} />
            <div className="form-check mt-1">
              <input
                className="form-check-input"
                type="checkbox"
                id="silently"
                name="silently"
                checked={silently}
                onChange={(e) => setSilently(e.target.checked)}
              />
              <label className="form-check-label" htmlFor="silently">
                {gettext('Add member silently')}
              </label>
            </div>
          </div>
        )}
        {errors.non_field_errors?.map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))}
      </form>
    </Modal>
  )
}

MembershipInviteModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
}

export default MembershipInviteModal
