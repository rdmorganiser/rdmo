import React, { useState } from 'react'
import { useSelector } from 'react-redux'

import { useModal } from 'rdmo/core/assets/js/hooks'

import IntegrationsDropdown from '../helper/IntegrationsDropdown'

import IntegrationDeleteModal from './integrations/IntegrationDeleteModal'
import IntegrationModal from './integrations/IntegrationModal'

const Integrations = () => {
  const perms = useSelector((state) => state.project.project.project.permissions) ?? {}
  const providers = useSelector((state) => state.project.providers) ?? {}
  const integrations = useSelector((state) => state.project.integrations) ?? []

  const [providerKey, setProviderKey] = useState(null)
  const [selectedIntegration, setSelectedIntegration] = useState(null)

  const createModal = useModal()
  const updateModal = useModal()
  const deleteModal = useModal()

  const hasProviders = Object.keys(providers).length > 0
  const visibleIntegrations = integrations.filter((integration) => integration.provider)

  const handleProviderChange = (value) => {
    setProviderKey(value)
    createModal.open()
  }

  const openUpdateModal = (integration) => {
    setSelectedIntegration(integration)
    updateModal.open()
  }

  const openDeleteModal = (integration) => {
    setSelectedIntegration(integration)
    deleteModal.open()
  }

  return (
    <div className="project-integrations">
      <div className="d-lg-flex justify-content-between align-items-center mb-5">
        <h1 className="mb-lg-0">{gettext('Integrations')}</h1>
        {
          perms.can_add_integration && hasProviders && (
            <IntegrationsDropdown providers={providers} onChange={handleProviderChange} />
          )
        }
      </div>

      {
        perms.can_view_integration && (
          <>
            <h2>{gettext('Added integrations')}</h2>
            <p className="text-muted">
              {
                gettext(
                  'Integrations can be used to send tasks to various external tools. ' +
                  'Please follow the descriptions of the integrations to use them.'
                )
              }
            </p>
            {
              visibleIntegrations.length > 0 && (
                <table className="table">
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
              )
            }
          </>
        )
      }

      <IntegrationModal
        show={createModal.show}
        onClose={createModal.close}
        providerKey={providerKey}
      />

      {
        selectedIntegration && (
          <>
            <IntegrationModal
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
