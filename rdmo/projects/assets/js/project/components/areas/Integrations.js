import React, { useState } from 'react'
import { useSelector } from 'react-redux'

import { useModal } from 'rdmo/core/assets/js/hooks'

import { usePermissions } from '../../hooks'

import IntegrationsDropdown from '../helper/IntegrationsDropdown'

import IntegrationDeleteModal from './integrations/IntegrationDeleteModal'
import IntegrationModal from './integrations/IntegrationModal'
import IntegrationTable from './integrations/IntegrationTable'

const Integrations = () => {
  const perms = usePermissions()
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
                <IntegrationTable
                  integrations={visibleIntegrations}
                  onUpdate={perms.can_change_integration ? openUpdateModal : null}
                  onDelete={perms.can_delete_integration ? openDeleteModal : null}
                />
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
