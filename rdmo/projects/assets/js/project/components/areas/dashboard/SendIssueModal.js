import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import { Input, Textarea } from 'rdmo/core/assets/js/components/forms'

import { fetchProjectFiles } from '../../../actions/projectActions'

import SendIssueDropdowns from './SendIssueDropdowns'

const SendIssueModal = ({
  issue,
  onClose
}) => {
  const dispatch = useDispatch()
  const project = useSelector((state) => state.project.project.project)
  const currentUser = useSelector((state) => state.user.currentUser) ?? {}
  const settings = useSelector(state => state.settings)
  const sites = useSelector(state => state.sites) ?? {}
  const currentSite = Object.values(sites).find((site) => site.id === project.site)

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

  const hasRecipientChoices = settings.email_recipients?.length > 0
  const hasRecipientInput = settings.email_recipients_input
  const hasMail = hasRecipientChoices || hasRecipientInput
  /* TODO: fetch attached integrations to determine boolean; setting is not enough */
  const hasIntegrations = settings.project_issue_providers?.length > 0
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
    attachments_format: null,

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

  const handleSend = (extraPayload = {}) => {
    const attachmentsFiles = formData.attachments_files_by_snapshot[formData.attachments_snapshot] || []
    const payload = {
      subject: formData.subject,
      message: formData.message,
      attachments_answers: formData.attachments_answers,
      attachments_views: formData.attachments_views,
      attachments_files: attachmentsFiles,
      attachments_snapshot: formData.attachments_snapshot,
      attachments_format: formData.attachments_format,
      ...extraPayload
    }

    console.log(payload)
  }

  const handleSendMail = () => {
    handleSend({
      recipients: formData.recipients,
      recipients_input: formData.recipients_input
    })
  }

  const handleSendIntegration = (providerKey, providerClass) => {
    handleSend({
      provider: providerKey,
      provider_class: providerClass
    })
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
        {/* TODO: use a template for that? */}
        {
          !isConfigured && (
            <p className="text-muted">
              {gettext('The send task functionality is not properly configured yet.')}
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
              {/* TODO: use a template for that? */}
              <p>{gettext('Sending a task will set the status to "in progress".')}</p>
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
                rows="5"
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
              <div className="form-label fw-bold">
                {gettext('Recipients')}
              </div>
              {
                hasRecipientChoices && (
                  <div className="mb-3">
                    {
                      settings.email_recipients.map(([value, label], index) => (
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
                  <>
                    {/* TODO: use a template for placeholder? */}
                    <Textarea
                      className="mb-3"
                      rows="3"
                      placeholder={gettext('Enter recipients line by line')}
                      value={formData.recipients_input}
                      onChange={(value) => setField('recipients_input', value)}
                    />
                  </>
                )
              }

              <div className="mb-4 text-end">
                <button
                  disabled={!canSendMail}
                  type="button"
                  className="btn btn-primary"
                  onClick={handleSendMail}
                >
                  {gettext('Send by mail')}
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
                {
                  /* TODO: switch to attached integrations and its structure */
                  settings.project_issue_providers.map(([key, label, provider]) => (
                    <div className="row align-items-center mb-3" key={key}>
                      <div className="col">
                        {label}
                      </div>
                      <div className="col text-end">
                        <button
                          type="button"
                          className="btn btn-primary"
                          onClick={() => handleSendIntegration(key, provider)}
                        >
                          {interpolate(gettext('Send to %s'), [label])}
                        </button>
                      </div>
                    </div>
                  ))
                }
              </div>
            </>
          )
        }
      </form>
    </Modal>
  )
}

SendIssueModal.propTypes = {
  issue: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired
}

export default SendIssueModal
