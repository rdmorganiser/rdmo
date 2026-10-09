import React from 'react'
import PropTypes from 'prop-types'

const IntegrationTable = ({ integrations, onDelete, onOpen, onUpdate }) => {

  return (
    <table className="table">
      <thead>
        <tr>
          <th style={{ width: '10%' }}>{gettext('Integration')}</th>
          <th style={{ width: '45%' }}>{gettext('Description')}</th>
          <th style={{ width: '35%' }}>{gettext('Options')}</th>
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
              <td>{integration.provider.description}</td>
              <td>
                {
                  integration.options
                    .filter((option) => !option.secret)
                    .map((option) => (
                      <p key={option.key}>{option.title}: {option.value}</p>
                    ))
                }
              </td>
              <td>
                <div className="d-flex justify-content-end align-items-center gap-1">
                  <button
                    type="button"
                    className="link"
                    aria-label={gettext('View integration')}
                    title={gettext('View integration')}
                    onClick={() => onOpen(integration)}
                  >
                    <i className="bi bi-eye" aria-hidden="true" />
                  </button>
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
  onDelete: PropTypes.func,
  onOpen: PropTypes.func.isRequired,
  onUpdate: PropTypes.func
}

export default IntegrationTable
