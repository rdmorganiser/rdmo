import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import { Input } from 'rdmo/core/assets/js/components/forms'

import {
  clearProjectErrors,
  createProjectIntegration,
  updateProjectIntegration
} from '../../../actions/projectActions'
import { useFieldErrors } from '../../../hooks/useFieldErrors'

const IntegrationModal = ({ show, onClose, providerKey, integration }) => {
  const dispatch = useDispatch()
  const providers = useSelector((state) => state.project.providers) ?? {}
  const errors = useFieldErrors()

  const [title, setTitle] = useState('')
  const [optionValues, setOptionValues] = useState({})
  const [replaceSecrets, setReplaceSecrets] = useState({})

  const isEdit = !!(integration && integration.id)
  const currentProviderKey = integration?.provider_key ?? providerKey
  const provider = providers[currentProviderKey]
  const formId = isEdit ? 'update-integration-form' : 'create-integration-form'

  useEffect(() => {
    if (show && provider) {
      setTitle(integration?.title ?? provider.label)
      setOptionValues(Object.fromEntries(
        provider.fields.map((field) => {
          const option = integration?.options.find((item) => item.key === field.key)
          return [field.key, option?.secret ? '' : option?.value ?? '']
        })
      ))
      setReplaceSecrets({})
      dispatch(clearProjectErrors())
    }
  }, [show, integration, provider, dispatch])

  const hasStoredSecret = (key) => isEdit && integration.options.some(
    (option) => option.key === key && option.secret && option.configured
  )

  const setField = (key, value) => {
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
    setField(key, '')
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

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

    const data = {
      title,
      provider_key: currentProviderKey,
      options
    }

    try {
      if (isEdit) {
        await dispatch(updateProjectIntegration(integration.id, data))
      } else {
        await dispatch(createProjectIntegration(data))
      }
      onClose()
    } catch {
      // keep modal open; errors are shown via useFieldErrors
    }
  }

  return (
    <Modal
      title={isEdit ? gettext('Update integration') : provider?.add_label ?? gettext('Add integration')}
      show={show}
      onClose={onClose}
      onSubmit={() => { }} // render the Modal's submit button
      submitLabel={isEdit ? gettext('Update integration') : gettext('Add integration')}
      submitProps={{ type: 'submit', form: formId }}
      size="modal-lg"
    >
      <form id={formId} onSubmit={handleSubmit}>
        <p className="text-muted">{provider?.description}</p>

        <Input
          type="text"
          className="mb-3"
          label={`${gettext('Title')} *`}
          value={title}
          onChange={setTitle}
          errors={errors.title}
        />

        {
          provider?.fields.map((field) => {
            const storedSecret = field.secret && hasStoredSecret(field.key)
            const replaceSecret = replaceSecrets[field.key] ?? false
            const switchId = `replace-integration-${integration?.id}-${field.key}`

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
                      onChange={(value) => setField(field.key, value)}
                      errors={errors[field.key]}
                    />
                  )
                }
              </div>
            )
          })
        }

        {
          [...(errors.options ?? []), ...(errors.non_field_errors ?? [])].map((error, index) => (
            <div key={index} className="text-danger mt-1">{error}</div>
          ))
        }
      </form>
    </Modal>
  )
}

IntegrationModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  providerKey: PropTypes.string,
  integration: PropTypes.object
}

export default IntegrationModal
