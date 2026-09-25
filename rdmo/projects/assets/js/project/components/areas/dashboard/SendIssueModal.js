import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { Modal } from 'rdmo/core/assets/js/components'
import { Input, Textarea } from 'rdmo/core/assets/js/components/forms'

import Select from 'rdmo/core/assets/js/components/forms/Select'
import Html from 'rdmo/core/assets/js/components/Html'

import { fetchProjectFiles, sendProjectIssueEmail, sendProjectIssueIntegration } from '../../../actions/projectActions'
import { useFieldErrors } from '../../../hooks'

import SendIssueDropdowns from './SendIssueDropdowns'

const SendIssueModal = ({
  issue,
  onClose
}) => {
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
  const externalResources = issue?.resources.map(item => item.integration) ?? []
  const integrationOptions = visibleIntegrations.map((integration) => ({
    value: integration.id,
    label: integration.title,
    integration
  }))

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
  const [sendMethod, setSendMethod] = useState(hasMail ? 'mail' : 'integration')
  const [integration, setIntegration] = useState(null)
  const selectedIntegration = visibleIntegrations.find((item) => item.id === integration)

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

  const handleSendIntegration = async (integration) => {
    const payload = getPayload({
      integration: integration.id
    })

    try {
      await dispatch(sendProjectIssueIntegration(issue.id, payload))
      onClose()
    } catch {
      // Keep the modal open so the error can be displayed.
    }
  }

  const handleIntegrationChange = (integrationId) => {
    setIntegration(integrationId)
  }

  const formatIntegrationOption = ({ integration }, { context }) => {
    if (context === 'value') {
      return integration.title
    }

    return (
      <div className="py-1">
        <div className="fw-semibold">{integration.title}</div>
        <div className="text-muted font-smaller">{integration.provider.description}</div>
        {
          integration.options
            .filter((option) => !option.secret)
            .map((option) => (
              <div className="font-smaller" key={option.key}>
                {option.title}: {option.value}
              </div>
            ))
        }
        {
          externalResources.includes(integration.id) && (
            <div className="alert alert-warning py-1 px-2 mt-2 mb-0 font-smaller">
              <i className="bi bi-exclamation-triangle me-1" aria-hidden="true" />
              {gettext('This issue has already been sent using this integration.')}
            </div>
          )
        }
      </div>
    )
  }

  const filterIntegrationOption = ({ data }, inputValue) => {
    const integration = data.integration
    const options = integration.options.filter((option) => !option.secret)
    const searchValue = [
      integration.title,
      integration.provider.description,
      ...options.flatMap((option) => [option.title, option.value])
    ].filter(Boolean).join(' ').toLocaleLowerCase()

    return searchValue.includes(inputValue.trim().toLocaleLowerCase())
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
          hasMail && hasIntegrations && (
            <ul className="nav nav-tabs mb-4" role="tablist" aria-label={gettext('Send using')}>
              <li className="nav-item" role="presentation">
                <button
                  type="button"
                  className={classNames('nav-link', { active: sendMethod === 'mail' })}
                  role="tab"
                  aria-selected={sendMethod === 'mail'}
                  onClick={() => setSendMethod('mail')}
                >
                  {gettext('Send by mail')}
                </button>
              </li>
              <li className="nav-item" role="presentation">
                <button
                  type="button"
                  className={classNames('nav-link', { active: sendMethod === 'integration' })}
                  role="tab"
                  aria-selected={sendMethod === 'integration'}
                  onClick={() => setSendMethod('integration')}
                >
                  {gettext('Send by integration')}
                </button>
              </li>
            </ul>
          )
        }
        {
          hasMail && sendMethod === 'mail' && (
            <>
              <div className="fw-semibold mb-2">{gettext('Recipients')}</div>
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
              <div className="d-flex justify-content-end mt-4 mb-4">
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
          hasIntegrations && sendMethod === 'integration' && (
            <>
              <Select
                label={gettext('Integration')}
                placeholder={gettext('Select an integration...')}
                isDisabled={isSubmitting}
                options={integrationOptions}
                value={integration}
                filterOption={filterIntegrationOption}
                formatOptionLabel={formatIntegrationOption}
                onChange={handleIntegrationChange}
                isClearable
              />
              {
                selectedIntegration && (
                  <div className="border rounded p-3 mt-3">
                    <div className="fw-semibold mb-2">{selectedIntegration.title}</div>
                    <p>{selectedIntegration.provider.description}</p>
                    {
                      selectedIntegration.options
                        .filter((option) => !option.secret)
                        .map((option) => (
                          <div key={option.key}>{option.title}: {option.value}</div>
                        ))
                    }
                    {
                      externalResources.includes(selectedIntegration.id) && (
                        <div className="alert alert-warning py-2 px-3 mt-3 mb-0">
                          <i className="bi bi-exclamation-triangle me-2" aria-hidden="true" />
                          {gettext('This issue has already been sent using this integration.')}
                        </div>
                      )
                    }
                  </div>
                )
              }
              {
                selectedIntegration && (
                  <div className="d-flex justify-content-end mt-4 mb-4">
                    <button
                      disabled={isSubmitting}
                      type="button"
                      className="btn btn-primary"
                      onClick={handleSendIntegration}
                    >
                      {selectedIntegration.provider.send_label ?? gettext('Send by integration')}
                    </button>
                  </div>
                )
              }
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
