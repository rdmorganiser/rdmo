import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { Modal } from 'rdmo/core/assets/js/components'
import { Input, Textarea } from 'rdmo/core/assets/js/components/forms'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchProjectFiles, sendProjectIssueEmail } from '../../../actions/projectActions'
import { useFieldErrors } from '../../../hooks'

import IntegrationTable from '../integrations/IntegrationTable'

import SendIssueDropdowns from './SendIssueDropdowns'

const SendIssueModal = ({
  issue,
  onClose
}) => {
  console.log('issue', issue.id)
  const dispatch = useDispatch()
  const project = useSelector(state => state.project.project.project)
  const currentUser = useSelector(state => state.user.currentUser) ?? {}
  const templates = useSelector(state => state.templates)
  const settings = useSelector(state => state.settings)
  const sites = useSelector(state => state.sites) ?? {}
  const isSubmitting = useSelector(state => state.pending.items.includes('sendProjectIssueEmail'))
  const currentSite = Object.values(sites).find(site => site.id === project.site)
  const integrations = useSelector(state => state.project.integrations) ?? []
  const errors = useFieldErrors()

  /* TODO: use templates? */
  const initialMessage = [
    gettext('To whom it may concern,'),
    '',
    gettext('The following task was identified in the project'),
    `"${project.title}" <${window.location.origin + `/projects/${project.id}/`}>:`,
    '',
    issue.task.text || '',
    '',
    gettext('Sincerely,'),
    `    ${[currentUser.first_name, currentUser.last_name].filter(Boolean).join(' ') || currentUser.username || ''}`,
    '',
    '--',
    interpolate(
      gettext('This message was generated using %s at %s.'),
      [currentSite?.name || currentSite?.domain || '', window.location.origin + '/']
    )
  ].join('\n')

  const hasRecipientChoices = !isEmpty(settings.email_recipients_choices)
  const hasRecipientInput = settings.email_recipients_input
  const hasMail = hasRecipientChoices || hasRecipientInput
  const visibleIntegrations = integrations.filter((integration) => integration.provider)
  const hasIntegrations = visibleIntegrations.length > 0
  const isConfigured = hasMail || hasIntegrations

  const [formData, setFormData] = useState({
    subject: issue.task.title || '',
    message: initialMessage,

    attachments_answers: [],
    attachments_views: [],
    attachments_files_by_snapshot: {
      current: []
    },
    attachments_snapshot: 'current',
    // as (required) format checkboxes are "hidden" in a dropdown, better set a default value
    attachments_format: settings.export_formats?.[0]?.[0] ?? null,

    recipients: [],
    recipients_input: ''
  })

  const canSendMail =
    formData.recipients.length > 0 ||
    formData.recipients_input.trim() !== ''

  const setField = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }))
  }

  const handleCheckboxChange = (key, value, checked) => {
    setFormData(prev => ({
      ...prev,
      [key]: checked ? [...prev[key], value] : prev[key].filter(item => item !== value)
    }))
  }

  const handleFileChange = (fileId, checked) => {
    setFormData(prev => {
      const snapshotId = prev.attachments_snapshot
      const selectedFiles = prev.attachments_files_by_snapshot[snapshotId] || []

      return {
        ...prev,
        attachments_files_by_snapshot: {
          ...prev.attachments_files_by_snapshot,
          [snapshotId]: checked ? [...selectedFiles, fileId] : selectedFiles.filter(id => id !== fileId)
        }
      }
    })
  }

  const handleSnapshotChange = (snapshotId) => {
    setField('attachments_snapshot', snapshotId)
    dispatch(fetchProjectFiles(snapshotId === 'current' ? undefined : snapshotId))
  }

  const getPayload = (extraPayload = {}) => {
    const attachmentsFiles = formData.attachments_files_by_snapshot[formData.attachments_snapshot] || []

    return {
      subject: formData.subject,
      message: formData.message,
      attachments_answers: formData.attachments_answers,
      attachments_views: formData.attachments_views,
      attachments_files: attachmentsFiles,
      attachments_snapshot: formData.attachments_snapshot,
      attachments_format: formData.attachments_format,
      ...extraPayload
    }

  }

  const handleSendMail = async () => {
    const payload = getPayload({
      recipients: formData.recipients,
      recipients_input: formData.recipients_input
    })

    try {
      await dispatch(sendProjectIssueEmail(issue.id, payload))
      onClose()
    } catch {
      // Keep the modal open so the error can be displayed.
    }
  }

  const handleSendIntegration = () => {
    const payload = getPayload({
    })

    console.log('payload', payload)
  }

  return (
    <Modal
      show
      title={gettext('Send task')}
      onClose={onClose}
      closeLabel={gettext('Close')}
      size="modal-lg"
    >
      <form>
        {
          !isConfigured && (
            <p className="text-muted">
              <Html html={templates.project_issue_config_info} />
            </p>
          )
        }
        {
          isConfigured && (
            <>
              <SendIssueDropdowns
                formData={formData}
                setField={setField}
                onCheckboxChange={handleCheckboxChange}
                onSnapshotChange={handleSnapshotChange}
                onFileChange={handleFileChange}
                formats={settings.export_formats ?? []}
              />
              <Html html={templates.project_issue_send_info} />
              <Input
                className="mb-3"
                label={gettext('Subject')}
                type="text"
                value={formData.subject}
                onChange={(value) => setField('subject', value)}
              />

              <Textarea
                className="mb-4"
                label={gettext('Message')}
                rows="12"
                value={formData.message}
                onChange={(value) => setField('message', value)}
              />
            </>
          )
        }
        {
          hasMail && (
            <>
              <h2>{gettext('Send by mail')}</h2>
              <div className="fw-semibold mb-2">
                {gettext('Recipients')}
              </div>
              {
                hasRecipientChoices && (
                  <div>
                    {
                      settings.email_recipients_choices.map(([value, label], index) => (
                        <div className="form-check" key={value}>
                          <input
                            id={`id_recipients_${index}`}
                            name="recipients"
                            type="checkbox"
                            className="form-check-input"
                            value={value}
                            checked={formData.recipients.includes(value)}
                            onChange={(event) => handleCheckboxChange('recipients', value, event.target.checked)}
                          />
                          <label className="form-check-label fw-normal" htmlFor={`id_recipients_${index}`}>
                            {label}
                          </label>
                        </div>
                      ))
                    }
                  </div>
                )
              }
              {
                hasRecipientInput && (
                  <Textarea
                    className="mb-3"
                    rows="3"
                    placeholder={gettext('Enter recipients line by line')}
                    value={formData.recipients_input}
                    onChange={(value) => setField('recipients_input', value)}
                  />
                )
              }

              <div className="mb-4 text-end">
                <button
                  disabled={!canSendMail || isSubmitting}
                  type="button"
                  className="btn btn-primary"
                  onClick={handleSendMail}
                >
                  {
                    isSubmitting ? (
                      <>
                        <span
                          className="spinner-border spinner-border-sm me-2"
                          role="status"
                          aria-hidden="true"
                        />
                        {gettext('Sending...')}
                      </>
                    ) : gettext('Send by mail')
                  }
                </button>
              </div>
            </>
          )
        }

        {
          hasIntegrations && (
            <>
              <h2>{gettext('Send via integration')}</h2>

              <div className="mb-4">
                <IntegrationTable
                  integrations={visibleIntegrations}
                  onSend={handleSendIntegration}
                />
              </div>
            </>
          )
        }
      </form>
      {
        Object.entries(errors).flatMap(([field, fieldErrors]) => (
          fieldErrors.map((error, index) => (
            <div key={`${field}-${index}`} className="text-danger mt-1">{error}</div>
          ))
        ))
      }
    </Modal>
  )
}

SendIssueModal.propTypes = {
  issue: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired
}

export default SendIssueModal
