import React from 'react'
import PropTypes from 'prop-types'

import { Modal } from 'rdmo/core/assets/js/components'

const IntegrationDetailsModal = ({ show, onClose, integration }) => {
  return (
    <Modal
      title={integration.title}
      show={show}
      onClose={onClose}
      closeLabel={gettext('Close')}
      size="modal-lg"
    >
      <p className="text-muted mb-4">{integration.provider.description}</p>

      <dl>
        {
          integration.options.map((option) => (
            <div key={option.key}>
              <dt>{option.title}</dt>
              <dd>
                {
                  option.secret ? (
                    option.configured ? gettext('Configured') : gettext('Not configured')) : option.value
                }
              </dd>
            </div>
          ))
        }
        {
          integration.webhook && (
            <div>
              {
                integration.webhook.description && (
                  <div>
                    <dt>{gettext('Webhook information')}</dt>
                    <dd>{integration.webhook.description}</dd>
                  </div>
                )
              }
              <dt>{gettext('Payload URL')}</dt>
              <dd className="font-monospace text-break user-select-all">
                {integration.webhook.url}
              </dd>
            </div>
          )
        }
      </dl>
    </Modal>
  )
}

IntegrationDetailsModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  integration: PropTypes.object.isRequired
}

export default IntegrationDetailsModal
