import React from 'react'
import PropTypes from 'prop-types'

const IntegrationTable = ({ integrations, externalResources, onDelete, onSend, onUpdate }) => {

  return (
    <table className="table">
      <thead>
        <tr>
          <th style={{ width: '10%' }}>{gettext('Integration')}</th>
          <th style={{ width: '40%' }}>{gettext('Description')}</th>
          <th style={{ width: '40%' }}>{gettext('Options')}</th>
          <th style={{ width: '10%' }}>
            <span className="visually-hidden">{gettext('Actions')}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        {
          integrations.map((integration) => (
            <tr key={integration.id}>
              <td>{integration.title}</td>
              <td>{integration.provider?.description}</td>
              <td>
                {
                  integration.options
                    .filter((option) => !option.secret)
                    .map((option) => (
                      <p key={option.key}>{option.title}: {option.value}</p>
                    ))
                }
                {
                  externalResources?.length > 0 && externalResources.includes(integration.id) && (
                    <div className="text-muted">
                      {gettext('This issue has already been send using this integration.')}
                    </div>
                  )
                }
              </td>
              <td>
                <div className="d-flex justify-content-end align-items-center gap-1">
                  {
                    onSend ? (
                      <button
                        type="button"
                        className="btn btn-primary btn-sm font-smaller text-nowrap"
                        onClick={() => onSend(integration)}
                      >
                        {integration.provider.send_label}
                      </button>
                    ) : (
                      <>
                        {
                          onUpdate && (
                            <button
                              type="button"
                              className="link"
                              aria-label={gettext('Update integration')}
                              title={gettext('Update integration')}
                              onClick={() => onUpdate(integration)}
                            >
                              <i className="bi bi-pencil" aria-hidden="true" />
                            </button>
                          )
                        }
                        {
                          onDelete && (
                            <button
                              type="button"
                              className="link"
                              aria-label={gettext('Delete integration')}
                              title={gettext('Delete integration')}
                              onClick={() => onDelete(integration)}
                            >
                              <i className="bi bi-trash" aria-hidden="true" />
                            </button>
                          )
                        }
                      </>
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

IntegrationTable.propTypes = {
  integrations: PropTypes.array.isRequired,
  externalResources: PropTypes.array,
  onDelete: PropTypes.func,
  onSend: PropTypes.func,
  onUpdate: PropTypes.func
}

export default IntegrationTable
