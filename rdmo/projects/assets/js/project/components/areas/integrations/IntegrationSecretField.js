import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'

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

  return (
    <div>
      {
        configured && action === 'keep' && (
          <div className="mb-3">
            <label className="control-label" htmlFor={`${id}-current`}>
              {field.title}{field.required ? ' *' : ''}
            </label>
            <div className="input-group">
              <input
                id={`${id}-current`}
                type="password"
                className="form-control"
                value="configured"
                aria-label={`${field.title}: ${gettext('Secret is configured')}`}
                readOnly
              />
              <button
                type="button"
                className="btn btn-outline-secondary"
                title={gettext('Replace current secret')}
                aria-label={gettext('Replace current secret')}
                onClick={() => onActionChange('replace')}
              >
                <i className="bi bi-pencil" aria-hidden="true" />
              </button>
              {
                !field.required && (
                  <button
                    type="button"
                    className="btn btn-outline-secondary"
                    title={gettext('Remove current secret')}
                    aria-label={gettext('Remove current secret')}
                    onClick={() => onActionChange('remove')}
                  >
                    <i className="bi bi-trash" aria-hidden="true" />
                  </button>
                )
              }
            </div>
          </div>
        )
      }

      {
        inputVisible && (
          <div className="form-group mb-3">
            <label className="control-label" htmlFor={`${id}-input`}>
              {configured ? interpolate(gettext('New %s'), [field.title]) : field.title}
              {field.required || configured ? ' *' : ''}
            </label>
            <div className="input-group has-validation">
              <input
                id={`${id}-input`}
                type={showSecret ? 'text' : 'password'}
                className={errors?.length ? 'form-control is-invalid' : 'form-control'}
                placeholder={field.placeholder}
                value={value}
                onChange={(event) => onChange(event.target.value)}
              />
              <button
                type="button"
                className="btn btn-outline-secondary"
                title={showSecret ? gettext('Hide secret') : gettext('Show secret')}
                aria-label={showSecret ? gettext('Hide secret') : gettext('Show secret')}
                disabled={!value}
                onClick={() => setShowSecret(!showSecret)}
              >
                <i className={`bi ${showSecret ? 'bi-eye-slash' : 'bi-eye'}`} aria-hidden="true" />
              </button>
              <button
                type="button"
                className="btn btn-outline-secondary"
                title={configured ? gettext('Keep current secret') : gettext('Clear secret')}
                aria-label={configured ? gettext('Keep current secret') : gettext('Clear secret')}
                disabled={!configured && !value}
                onClick={() => configured ? onActionChange('keep') : onChange('')}
              >
                <i className="bi bi-x-lg" aria-hidden="true" />
              </button>
              {
                errors && (
                  <div className="invalid-feedback">
                    {errors.map((error, index) => <div key={index}>{error}</div>)}
                  </div>
                )
              }
            </div>
            {
              field.help && <div className="form-text">{field.help}</div>
            }
          </div>
        )
      }

      {
        configured && action === 'remove' && (
          <div className="mb-3">
            <label className="control-label" htmlFor={`${id}-current`}>
              {field.title}
            </label>
            <div className="input-group">
              <input
                id={`${id}-current`}
                type="password"
                className="form-control"
                value="configured"
                aria-label={`${field.title}: ${gettext('Secret is configured')}`}
                readOnly
              />
              <button
                type="button"
                className="btn btn-outline-secondary"
                title={gettext('Keep current secret')}
                aria-label={gettext('Keep current secret')}
                onClick={() => onActionChange('keep')}
              >
                <i className="bi bi-arrow-counterclockwise me-1" aria-hidden="true" />
                {gettext('Keep secret')}
              </button>
            </div>
            <div className="form-text text-danger">
              {gettext('The current secret will be removed when the integration is updated.')}
            </div>
          </div>
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
