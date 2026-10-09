import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

const IntegrationTable = ({ integrations, onDelete, onUpdate }) => {

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
              <td>
                <strong>{integration.title}</strong>
              </td>
              <td>{integration.provider.description}</td>
              <td>
                {
                  !isEmpty(integration.options) && (
                    <dl className="d-flex flex-wrap column-gap-3 row-gap-1 mb-0">
                      {
                        integration.options
                          .filter((option) => !option.secret)
                          .map((option) => (
                            <div key={option.key} className="d-flex gap-1">
                              <dt>{option.title}:</dt>
                              <dd className="mb-0">
                                {
                                  URL.canParse(option.value) ? (
                                    <a href={option.value} target="_blank" rel="noreferrer">{option.value}</a>
                                  ) : option.value
                                }
                              </dd>
                            </div>
                          ))
                      }
                    </dl>
                  )
                }
              </td>
              <td>
                <div className="d-flex justify-content-end align-items-center gap-1">
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
  onUpdate: PropTypes.func
}

export default IntegrationTable
