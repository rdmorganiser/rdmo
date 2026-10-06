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

      <div className="d-flex flex-column gap-3">
        {
          integration.options.map((option) => (
            <div key={option.key}>
              <div className="fw-semibold">{option.title}</div>
              <div>
                {
                  option.secret ? (
                    option.configured ? gettext('Configured') : gettext('Not configured')) : option.value
                }
              </div>
            </div>
          ))
        }
        {
          integration.webhook && (
            <div>
              <h3 className="mb-2">{gettext('Webhook')}</h3>
              <div className="ps-3">
                {
                  integration.webhook.description && (
                    <p className="mb-3">{integration.webhook.description}</p>
                  )
                }
                <div className="fw-semibold">
                  {gettext('Payload URL')}
                </div>
                <div className="font-monospace text-break user-select-all">
                  {integration.webhook.url}
                </div>
              </div>
            </div>
          )
        }
      </div>
    </Modal>
  )
}

IntegrationDetailsModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  integration: PropTypes.object.isRequired
}

export default IntegrationDetailsModal
