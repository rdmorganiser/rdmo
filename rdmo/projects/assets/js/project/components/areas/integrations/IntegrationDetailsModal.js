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

      <dl className="mb-0">
        {
          integration.options.map((option) => (
            <React.Fragment key={option.key}>
              <dt>{option.title}</dt>
              <dd>
                {
                  option.secret ? (
                    option.configured ? gettext('Configured') : gettext('Not configured')) : option.value
                }
              </dd>
            </React.Fragment>
          ))
        }
        {
          integration.webhook && (
            <>
              {
                integration.webhook.description && (
                  <>
                    <dt>{gettext('Webhook information')}</dt>
                    <dd>{integration.webhook.description}</dd>
                  </>
                )
              }
              <dt>{gettext('Payload URL')}</dt>
              <dd>
                <code className="text-break user-select-all text-bg-secondary">{integration.webhook.url}</code>
              </dd>
            </>
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
