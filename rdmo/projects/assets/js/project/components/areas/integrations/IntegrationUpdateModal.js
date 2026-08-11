import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import { Input } from 'rdmo/core/assets/js/components/forms'

import { clearProjectErrors, updateProjectIntegration } from '../../../actions/projectActions'
import { useFieldErrors } from '../../../hooks/useFieldErrors'

const IntegrationUpdateModal = ({ show, onClose, integration }) => {
  const dispatch = useDispatch()
  const providers = useSelector((state) => state.project.providers) ?? {}
  const isSubmitting = useSelector((state) => state.pending.items.includes('updateProjectIntegration'))
  const errors = useFieldErrors()

  const [optionValues, setOptionValues] = useState({})
  const [replaceSecrets, setReplaceSecrets] = useState({})

  const provider = providers[integration?.provider_key]
  const formId = `update-integration-${integration?.id}`

  useEffect(() => {
    if (show && provider) {
      setOptionValues(Object.fromEntries(
        provider.fields.map((field) => {
          const option = integration.options.find((item) => item.key === field.key)
          return [field.key, option?.secret ? '' : option?.value ?? '']
        })
      ))
      setReplaceSecrets({})
      dispatch(clearProjectErrors())
    }
  }, [show, integration, provider, dispatch])

  const hasStoredSecret = (key) => integration?.options.some(
    (option) => option.key === key && option.secret && option.configured
  )

  const hasChanges = provider?.fields.some((field) => {
    if (field.secret && hasStoredSecret(field.key)) {
      return replaceSecrets[field.key] ?? false
    }

    const option = integration?.options.find((item) => item.key === field.key)
    const initialValue = option?.value?.trim() ?? ''
    const currentValue = optionValues[field.key]?.trim() ?? ''
    return currentValue !== initialValue
  }) ?? false

  const requiredFieldsComplete = provider?.fields.every((field) => {
    const valueEntered = !!optionValues[field.key]?.trim()

    if (field.secret && hasStoredSecret(field.key)) {
      if (!replaceSecrets[field.key] || !field.required) {
        return true
      }
      return valueEntered
    }

    return field.required ? valueEntered : true
  }) ?? false

  const handleOptionChange = (key, value) => {
    setOptionValues((currentValues) => ({
      ...currentValues,
      [key]: value
    }))
  }

  const handleReplaceSecretChange = (key, replace) => {
    setReplaceSecrets((currentValues) => ({
      ...currentValues,
      [key]: replace
    }))
    setOptionValues((currentValues) => ({
      ...currentValues,
      [key]: ''
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!provider || !requiredFieldsComplete || !hasChanges || isSubmitting) {
      return
    }

    const options = provider.fields
      .filter((field) => {
        if (field.secret && hasStoredSecret(field.key)) {
          return replaceSecrets[field.key]
        }
        return field.required || optionValues[field.key]?.trim()
      })
      .map((field) => ({
        key: field.key,
        value: optionValues[field.key]
      }))

    try {
      await dispatch(updateProjectIntegration(integration.id, {
        provider_key: integration.provider_key,
        options
      }))
      onClose()
    } catch {
      // Keep the modal open so errors can be corrected and submitted again.
    }
  }

  return (
    <Modal
      title={gettext('Update integration')}
      show={show}
      onClose={onClose}
      onSubmit={() => { }}
      submitLabel={gettext('Update integration')}
      submitProps={
        {
          type: 'submit',
          form: formId,
          disabled: !requiredFieldsComplete || !hasChanges || isSubmitting
        }
      }
      size="modal-lg"
    >
      <form id={formId} onSubmit={handleSubmit}>
        <p className="text-muted">{provider?.description}</p>

        {
          provider?.fields.map((field) => {
            const storedSecret = field.secret && hasStoredSecret(field.key)
            const replaceSecret = replaceSecrets[field.key] ?? false
            const switchId = `replace-integration-${integration.id}-${field.key}`

            return (
              <div key={field.key}>
                {
                  storedSecret && (
                    <>
                      <div className="mb-2">
                        {gettext('Current secret:')} <span aria-hidden="true">••••••••</span>
                        <span className="visually-hidden">{gettext('Secret is configured')}</span>
                      </div>
                      <div className="form-check form-switch mb-3">
                        <input
                          id={switchId}
                          type="checkbox"
                          className="form-check-input"
                          checked={replaceSecret}
                          onChange={(event) => handleReplaceSecretChange(field.key, event.target.checked)}
                        />
                        <label className="form-check-label" htmlFor={switchId}>
                          {gettext('Change or remove current secret')}
                        </label>
                      </div>
                    </>
                  )
                }

                {
                  (!storedSecret || replaceSecret) && (
                    <Input
                      type={field.secret ? 'password' : 'text'}
                      className="mb-3"
                      label={
                        `${storedSecret ? interpolate(gettext('New %s'), [field.title]) : field.title}` +
                        `${field.required ? ' *' : ''}`
                      }
                      placeholder={field.placeholder}
                      help={
                        storedSecret && !field.required ? (
                          <>
                            {field.help && <>{field.help}<br /></>}
                            {gettext('Leave this field blank to remove the current secret.')}
                          </>
                        ) : field.help
                      }
                      value={optionValues[field.key] ?? ''}
                      onChange={(value) => handleOptionChange(field.key, value)}
                    />
                  )
                }
              </div>
            )
          })
        }

        {
          errors.non_field_errors?.map((error, index) => (
            <div key={index} className="text-danger mt-1">{error}</div>
          ))
        }
      </form>
    </Modal>
  )
}

IntegrationUpdateModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  integration: PropTypes.object.isRequired
}

export default IntegrationUpdateModal
