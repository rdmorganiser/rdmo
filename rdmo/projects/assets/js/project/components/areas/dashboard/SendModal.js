import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import { Input, Textarea } from 'rdmo/core/assets/js/components/forms'

const SendModal = ({
  issue,
  onClose
}) => {
  const project = useSelector((state) => state.project.project.project)
  const currentUser = useSelector((state) => state.user.currentUser) ?? {}
  const settings = useSelector(state => state.settings)
  const sites = useSelector(state => state.sites) ?? {}
  const answers = useSelector((state) => state.project.project.answers) ?? {}
  const views = useSelector((state) => state.project.project.views) ?? []
  const snapshots = useSelector((state) => state.project.project.snapshots) ?? []
  const files = []
  const formats = settings.export_formats ?? []
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
    `    ${currentUser.first_name || ''} ${currentUser.last_name || ''}`,
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
  const hasIntegrations = settings.project_issue_providers?.length > 0
  const isConfigured = hasMail || hasIntegrations

  const [formData, setFormData] = useState({
    subject: issue.task.title || '',
    message: initialMessage,

    attachments_answers: [],
    attachments_views: [],
    attachments_files: [],
    attachments_snapshot: null,
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

  const handleSend = (extraPayload = {}) => {
    const payload = {
      subject: formData.subject,
      message: formData.message,
      attachments_answers: formData.attachments_answers,
      attachments_views: formData.attachments_views,
      attachments_files: formData.attachments_files,
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
              <div className="d-flex justify-content-end gap-3 mb-3">
                <div className="dropdown">
                  <button
                    type="button"
                    className="link text-nowrap"
                    data-bs-toggle="dropdown"
                    data-bs-popper-config='{"strategy":"fixed"}'
                    aria-expanded="false"
                    title={gettext('Attachments')}
                  >
                    {gettext('Attachments')} <i className="bi bi-caret-down-fill ms-1" />
                  </button>

                  <div className="dropdown-menu p-3" style={{ minWidth: '280px' }}>
                    {
                      answers.html && (
                        <div className="mb-3">
                          <div className="fw-bold mb-2">
                            {gettext('Answers')}
                          </div>

                          <div className="form-check">
                            <input
                              id="id_attachments_answers"
                              name="attachments_answers"
                              type="checkbox"
                              className="form-check-input"
                              value="project_answers"
                              checked={formData.attachments_answers.includes('project_answers')}
                              onChange={
                                (event) => handleCheckboxChange(
                                  'attachments_answers',
                                  'project_answers',
                                  event.target.checked
                                )
                              }
                            />
                            <label
                              className="form-check-label fw-normal"
                              htmlFor="id_attachments_answers"
                            >
                              {/* TODO: use a template for that? */}
                              {gettext('Attach the output of "View answers".')}
                            </label>
                          </div>
                        </div>
                      )
                    }
                    {
                      views.length > 0 && (
                        <div className="mb-3">
                          <div className="fw-bold mb-2">{gettext('Views')}</div>
                          {
                            views.map((view) => (
                              <div className="form-check" key={view.id}>
                                <input
                                  id={`id_attachments_views_${view.id}`}
                                  name="attachments_views"
                                  type="checkbox"
                                  className="form-check-input"
                                  value={view.id}
                                  checked={formData.attachments_views.includes(view.id)}
                                  onChange={
                                    (event) => handleCheckboxChange('attachments_views', view.id, event.target.checked)
                                  }
                                />
                                <label
                                  className="form-check-label fw-normal"
                                  htmlFor={`id_attachments_views_${view.id}`}>
                                  {view.title}
                                </label>
                              </div>
                            ))
                          }
                        </div>
                      )
                    }

                    {
                      files.length > 0 && (
                        <div className="mb-3">
                          <div className="fw-bold mb-2">{gettext('Files')}</div>
                          {
                            files.map((file) => (
                              <div className="form-check" key={file.id}>
                                <input
                                  id={`id_attachments_files_${file.id}`}
                                  name="attachments_files"
                                  type="checkbox"
                                  className="form-check-input"
                                  value={file.id}
                                  checked={formData.attachments_files.includes(file.id)}
                                  onChange={
                                    (event) => handleCheckboxChange('attachments_files', file.id, event.target.checked)
                                  }
                                />
                                <label
                                  className="form-check-label fw-normal"
                                  htmlFor={`id_attachments_files_${file.id}`}>
                                  {file.file_name}
                                </label>
                              </div>
                            ))
                          }
                        </div>
                      )
                    }

                    {
                      snapshots.length > 0 && (
                        <div>
                          <div className="fw-bold mb-2">{gettext('Snapshot')}</div>
                          {
                            snapshots.map((snapshot) => (
                              <div className="form-check" key={snapshot.id}>
                                <input
                                  id={`id_attachments_snapshot_${snapshot.id}`}
                                  name="attachments_snapshot"
                                  type="radio"
                                  className="form-check-input"
                                  value={snapshot.id}
                                  checked={formData.attachments_snapshot === snapshot.id}
                                  onChange={() => setField('attachments_snapshot', snapshot.id)}
                                />
                                <label
                                  className="form-check-label fw-normal"
                                  htmlFor={`id_attachments_snapshot_${snapshot.id}`}>
                                  {snapshot.title}
                                </label>
                              </div>
                            ))
                          }
                        </div>
                      )
                    }
                  </div>
                </div>
                <div className="dropdown">
                  <button
                    type="button"
                    className="link text-nowrap"
                    data-bs-toggle="dropdown"
                    data-bs-popper-config='{"strategy":"fixed"}'
                    aria-expanded="false"
                    title={gettext('Format')}
                  >
                    {gettext('Format')} <i className="bi bi-caret-down-fill ms-1" />
                  </button>

                  <div className="dropdown-menu p-3" style={{ minWidth: '220px' }}>
                    {
                      formats.map(([format, label]) => (
                        <div className="form-check" key={format}>
                          <input
                            id={`id_attachments_format_${format}`}
                            name="attachments_format"
                            type="radio"
                            className="form-check-input"
                            value={format}
                            checked={formData.attachments_format === format}
                            onChange={() => setField('attachments_format', format)}
                          />
                          <label
                            className="form-check-label fw-normal"
                            htmlFor={`id_attachments_format_${format}`}
                          >
                            {label}
                          </label>
                        </div>
                      ))
                    }
                  </div>
                </div>
              </div>
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

SendModal.propTypes = {
  issue: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired
}

export default SendModal
