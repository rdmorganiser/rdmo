import React from 'react'
import PropTypes from 'prop-types'

import Select from 'rdmo/core/assets/js/components/forms/Select'

const SendIssueIntegration = ({
  integrations,
  externalResources,
  value,
  onChange,
  disabled,
  errors
}) => {
  const integrationOptions = integrations.map((integration) => ({
    value: integration.id,
    label: integration.title,
    integration
  }))
  const selectedIntegration = integrations.find((integration) => integration.id === value)

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
              {gettext('This task has already been sent using this integration.')}
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
    <>
      <Select
        label={gettext('Integration')}
        placeholder={gettext('Select an integration...')}
        isDisabled={disabled}
        options={integrationOptions}
        value={value}
        filterOption={filterIntegrationOption}
        formatOptionLabel={formatIntegrationOption}
        onChange={onChange}
        isClearable
        errors={errors}
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
                  {gettext('This task has already been sent using this integration.')}
                </div>
              )
            }
          </div>
        )
      }
    </>
  )
}

SendIssueIntegration.propTypes = {
  integrations: PropTypes.array.isRequired,
  externalResources: PropTypes.array.isRequired,
  value: PropTypes.number,
  onChange: PropTypes.func.isRequired,
  disabled: PropTypes.bool.isRequired,
  errors: PropTypes.array
}

export default SendIssueIntegration
