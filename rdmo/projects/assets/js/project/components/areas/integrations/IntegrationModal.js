import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/components'
import { Input } from 'rdmo/core/assets/js/components/forms'

import {
  clearProjectErrors,
  createProjectIntegration,
  updateProjectIntegration
} from '../../../actions/projectActions'
import { useFieldErrors } from '../../../hooks/useFieldErrors'

import IntegrationSecretField from './IntegrationSecretField'

const IntegrationModal = ({ show, onClose, providerKey, integration }) => {
  const dispatch = useDispatch()
  const providers = useSelector((state) => state.project.providers) ?? {}
  const errors = useFieldErrors()

  const [title, setTitle] = useState('')
  const [optionValues, setOptionValues] = useState({})
  const [secretActions, setSecretActions] = useState({})

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
      setSecretActions({})
      dispatch(clearProjectErrors())
    }
  }, [show, integration, provider, dispatch])

  const hasStoredSecret = (key) => isEdit && integration.options.some(
    (option) => option.key === key && option.secret && option.configured
  )

  const setField = (key, value) => {
    setOptionValues(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const setSecretAction = (key, action) => {
    setSecretActions(prev => ({
      ...prev,
      [key]: action
    }))
    setField(key, '')
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    const options = provider.fields
      .filter((field) => {
        if (field.secret && hasStoredSecret(field.key)) {
          return ['replace', 'remove'].includes(secretActions[field.key])
        }
        return field.required || optionValues[field.key]?.trim()
      })
      .map((field) => {
        const option = { key: field.key }

        if (field.secret && secretActions[field.key] === 'remove') {
          option.remove = true
        } else {
          option.value = optionValues[field.key]
        }

        return option
      })

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
          help={gettext('A title for the integration.')}
        />

        {
          provider?.fields.map((field) => {
            const storedSecret = field.secret && hasStoredSecret(field.key)

            if (field.secret) {
              return (
                <IntegrationSecretField
                  key={field.key}
                  show={show}
                  formId={formId}
                  field={field}
                  configured={storedSecret}
                  value={optionValues[field.key] ?? ''}
                  action={secretActions[field.key] ?? 'keep'}
                  errors={errors[field.key]}
                  onChange={(value) => setField(field.key, value)}
                  onActionChange={(action) => setSecretAction(field.key, action)}
                />
              )
            }

            return (
              <Input
                key={field.key}
                type="text"
                className="mb-3"
                label={`${field.title}${field.required ? ' *' : ''}`}
                placeholder={field.placeholder}
                help={field.help}
                value={optionValues[field.key] ?? ''}
                onChange={(value) => setField(field.key, value)}
                errors={errors[field.key]}
              />
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
