import React, { useState } from 'react'
import PropTypes from 'prop-types'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import { Input, Textarea } from 'rdmo/core/assets/js/components/forms'

const SendModal = ({
  issue,
  settings,
  onClose
}) => {
  const hasRecipientChoices = settings.email_recipients?.length > 0
  const hasRecipientInput = settings.email_recipients_input
  const hasMail = hasRecipientChoices || hasRecipientInput
  const hasIntegrations = settings.project_issue_providers?.length > 0
  const isConfigured = hasMail || hasIntegrations

  const [formData, setFormData] = useState({
    subject: issue.task.title || '',
    message: issue.task.text || '',
    recipients: [],
    recipients_input: ''
  })

  const canSendMail =
    formData.recipients.length > 0 ||
    formData.recipients_input.trim() !== ''

  const setField = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }))
  }

  const handleRecipientChange = (value, checked) => {
    setFormData(prev => ({
      ...prev,
      recipients: checked ? [...prev.recipients, value] : prev.recipients.filter(recipient => recipient !== value)
    }))
  }

  const handleSendMail = () => {
    const payload = {
      subject: formData.subject,
      message: formData.message,
      recipients: formData.recipients,
      recipients_input: formData.recipients_input
    }

    console.log(payload)
  }

  const handleSendIntegration = (providerKey, providerClass) => {
    const payload = {
      subject: formData.subject,
      message: formData.message,
      provider: providerKey,
      provider_class: providerClass
    }

    console.log(payload)
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
                rows="10"
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
                            onChange={(event) => handleRecipientChange(value, event.target.checked)}
                          />
                          <label className="form-check-label" htmlFor={`id_recipients_${index}`}>
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
  settings: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired
}

export default SendModal
