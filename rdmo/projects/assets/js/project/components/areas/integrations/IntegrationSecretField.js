import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'

import { Input } from 'rdmo/core/assets/js/components/forms'

const IntegrationSecretField = ({
  show,
  formId,
  field,
  configured,
  value,
  action,
  errors,
  onChange,
  onActionChange
}) => {
  const [showSecret, setShowSecret] = useState(false)
  const inputVisible = !configured || action === 'replace'
  const id = `${formId}-${field.key}`

  useEffect(() => {
    if (show) {
      setShowSecret(false)
    }
  }, [show])

  useEffect(() => {
    if (!value) {
      setShowSecret(false)
    }
  }, [value])

  const actions = [
    { value: 'keep', label: gettext('Keep current secret') },
    { value: 'replace', label: gettext('Replace current secret') }
  ]

  if (!field.required) {
    actions.push({ value: 'remove', label: gettext('Remove current secret') })
  }

  return (
    <div>
      {
        configured && (
          <div className="mb-3">
            <label className="control-label">
              {field.title}{field.required ? ' *' : ''}
            </label>
            <div className="mb-3">
              {gettext('Current secret:')} <span aria-hidden="true">••••••••</span>
              <span className="visually-hidden">{gettext('Secret is configured')}</span>
            </div>

            {
              actions.map((option) => (
                <div className="form-check mb-1" key={option.value}>
                  <input
                    id={`${id}-${option.value}`}
                    type="radio"
                    name={`${id}-action`}
                    className="form-check-input"
                    checked={action === option.value}
                    onChange={() => onActionChange(option.value)}
                  />
                  <label className="form-check-label" htmlFor={`${id}-${option.value}`}>
                    {option.label}
                  </label>
                </div>
              ))
            }
          </div>
        )
      }

      {
        inputVisible && (
          <>
            <Input
              type={showSecret ? 'text' : 'password'}
              className="mb-1"
              label={
                `${configured ? interpolate(gettext('New %s'), [field.title]) : field.title}` +
                `${field.required || configured ? ' *' : ''}`
              }
              placeholder={field.placeholder}
              help={field.help}
              value={value}
              onChange={onChange}
              errors={errors}
              required={configured}
            />
            <div className="form-check mb-3">
              <input
                id={`${id}-show`}
                type="checkbox"
                className="form-check-input"
                checked={showSecret}
                disabled={!value}
                onChange={(event) => setShowSecret(event.target.checked)}
              />
              <label className="form-check-label" htmlFor={`${id}-show`}>
                {gettext('Show secret')}
              </label>
            </div>
          </>
        )
      }

      {
        configured && action === 'remove' && (
          <p className="text-danger mb-3">
            {gettext('The current secret will be removed when the integration is updated.')}
          </p>
        )
      }
    </div>
  )
}

IntegrationSecretField.propTypes = {
  show: PropTypes.bool.isRequired,
  formId: PropTypes.string.isRequired,
  field: PropTypes.object.isRequired,
  configured: PropTypes.bool.isRequired,
  value: PropTypes.string.isRequired,
  action: PropTypes.oneOf(['keep', 'replace', 'remove']).isRequired,
  errors: PropTypes.array,
  onChange: PropTypes.func.isRequired,
  onActionChange: PropTypes.func.isRequired
}

export default IntegrationSecretField
