import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { Input, Select } from 'rdmo/core/assets/js/components/forms'
import { useModal } from 'rdmo/core/assets/js/hooks'

import { createProjectIntegration } from '../../actions/projectActions'

import IntegrationDeleteModal from './integrations/IntegrationDeleteModal'
import IntegrationUpdateModal from './integrations/IntegrationUpdateModal'

const Integrations = () => {
  const dispatch = useDispatch()
  const perms = useSelector((state) => state.project.project.project.permissions) ?? {}
  const providers = useSelector((state) => state.project.providers) ?? {}
  const integrations = useSelector((state) => state.project.integrations) ?? []
  const isSubmitting = useSelector((state) => state.pending.items.includes('createProjectIntegration'))

  const [providerKey, setProviderKey] = useState(null)
  const [optionValues, setOptionValues] = useState({})
  const [selectedIntegration, setSelectedIntegration] = useState(null)

  const updateModal = useModal()
  const deleteModal = useModal()

  const providerOptions = Object.entries(providers).map(([key, provider]) => ({
    value: key,
    label: provider.add_label
  }))
  const provider = providers[providerKey]
  const visibleIntegrations = integrations.filter((integration) => integration.provider)
  const requiredFieldsComplete = provider?.fields
    .filter((field) => field.required)
    .every((field) => optionValues[field.key]?.trim()) ?? false

  const handleProviderChange = (value) => {
    setProviderKey(value)
    setOptionValues({})
  }

  const handleOptionChange = (key, value) => {
    setOptionValues((currentValues) => ({
      ...currentValues,
      [key]: value
    }))
  }

  const openUpdateModal = (integration) => {
    setSelectedIntegration(integration)
    updateModal.open()
  }

  const openDeleteModal = (integration) => {
    setSelectedIntegration(integration)
    deleteModal.open()
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!provider || !requiredFieldsComplete || isSubmitting) {
      return
    }

    const options = provider.fields
      .filter((field) => field.required || optionValues[field.key]?.trim())
      .map((field) => ({
        key: field.key,
        value: optionValues[field.key]
      }))

    try {
      await dispatch(createProjectIntegration({
        provider_key: providerKey,
        options
      }))
      setProviderKey(null)
      setOptionValues({})
    } catch {
      // Keep the form values so errors can be corrected and submitted again.
    }
  }

  return (
    <div className="project-integrations">
      <h1 className="mb-5">{gettext('Integrations')}</h1>

      {
        perms.can_add_integration && providerOptions.length > 0 && (
          <div className="card card-tile mb-4">
            <div className="card-body">
              <h2>{gettext('Add integration to project')}</h2>

              <form onSubmit={handleSubmit}>
                <Select
                  className="mb-3"
                  label={gettext('Provider')}
                  placeholder={gettext('Select provider')}
                  isClearable
                  options={providerOptions}
                  value={providerKey}
                  onChange={handleProviderChange}
                />

                {
                  provider && (
                    <>
                      <p className="text-muted">{provider.description}</p>

                      {
                        provider.fields.map((field) => (
                          <Input
                            key={field.key}
                            type={field.secret ? 'password' : 'text'}
                            className="mb-3"
                            label={`${field.title}${field.required ? ' *' : ''}`}
                            placeholder={field.placeholder}
                            help={field.help}
                            value={optionValues[field.key] ?? ''}
                            onChange={(value) => handleOptionChange(field.key, value)}
                          />
                        ))
                      }
                    </>
                  )
                }

                {
                  provider && (
                    <button
                      type="submit"
                      className="btn btn-primary"
                      disabled={!requiredFieldsComplete || isSubmitting}
                    >
                      {gettext('Add integration')}
                    </button>
                  )
                }
              </form>
            </div>
          </div>
        )
      }

      {
        perms.can_view_integration && visibleIntegrations.length > 0 && (
          <div className="card card-tile mb-4">
            <div className="card-body">
              <h2>{gettext('Added integrations')}</h2>
              <p className="text-muted">
                {
                  gettext(
                    'Integrations can be used to send tasks to various external tools. ' +
                  'Please follow the descriptions of the integrations to use them.'
                  )
                }
              </p>

              <div className="table-responsive">
                <table className="table mb-0">
                  <thead>
                    <tr>
                      <th style={{ width: '15%' }}>{gettext('Provider')}</th>
                      <th style={{ width: '45%' }}>{gettext('Description')}</th>
                      <th style={{ width: '30%' }}>{gettext('Options')}</th>
                      <th style={{ width: '10%' }}>
                        <span className="visually-hidden">{gettext('Actions')}</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {
                      visibleIntegrations.map((integration) => (
                        <tr key={integration.id}>
                          <td>
                            {integration.provider.label}
                            <div className="small text-muted">
                              {interpolate(gettext('Integration #%s'), [integration.id])}
                            </div>
                          </td>
                          <td>{integration.provider.description}</td>
                          <td>
                            {
                              integration.options
                                .filter((option) => !option.secret)
                                .map((option) => (
                                  <div key={option.key}>
                                    {option.title}:<br />
                                    {option.value}
                                  </div>
                                ))
                            }
                          </td>
                          <td>
                            <div className="d-flex justify-content-end align-items-center gap-1">
                              {
                                perms.can_change_integration && (
                                  <button
                                    type="button"
                                    className="link"
                                    aria-label={gettext('Update integration')}
                                    title={gettext('Update integration')}
                                    onClick={() => openUpdateModal(integration)}
                                  >
                                    <i className="bi bi-pencil" aria-hidden="true" />
                                  </button>
                                )
                              }
                              {
                                perms.can_delete_integration && (
                                  <button
                                    type="button"
                                    className="link"
                                    aria-label={gettext('Delete integration')}
                                    title={gettext('Delete integration')}
                                    onClick={() => openDeleteModal(integration)}
                                  >
                                    <i className="bi bi-trash" aria-hidden="true" />
                                  </button>
                                )
                              }
                            </div>
                          </td>
                        </tr>
                      ))
                    }
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )
      }

      {
        selectedIntegration && (
          <>
            <IntegrationUpdateModal
              show={updateModal.show}
              onClose={updateModal.close}
              integration={selectedIntegration}
            />
            <IntegrationDeleteModal
              show={deleteModal.show}
              onClose={deleteModal.close}
              integration={selectedIntegration}
            />
          </>
        )
      }
    </div>
  )
}

export default Integrations
