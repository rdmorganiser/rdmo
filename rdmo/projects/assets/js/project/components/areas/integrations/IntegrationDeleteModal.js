import React, { useEffect } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/components'

import Html from 'rdmo/core/assets/js/components/Html'

import { clearProjectErrors, deleteProjectIntegration } from '../../../actions/projectActions'
import { useFieldErrors } from '../../../hooks/useFieldErrors'

const IntegrationDeleteModal = ({ show, onClose, integration }) => {
  const dispatch = useDispatch()
  const isSubmitting = useSelector((state) => state.pending.items.includes('deleteProjectIntegration'))
  const errors = useFieldErrors()

  useEffect(() => {
    if (show) {
      dispatch(clearProjectErrors())
    }
  }, [show, dispatch])

  const handleSubmit = async () => {
    try {
      await dispatch(deleteProjectIntegration(integration.id))
      onClose()
    } catch {
      // Keep the modal open so the error can be displayed.
    }
  }

  return (
    <Modal
      title={gettext('Delete integration')}
      show={show}
      onClose={onClose}
      onSubmit={handleSubmit}
      submitLabel={gettext('Delete integration')}
      submitProps={{ className: 'btn btn-danger', disabled: isSubmitting }}
      size="modal-lg"
    >
      <Html
        html={
          interpolate(
            gettext('You are about to permanently delete the <b>%s</b> integration.'),
            [integration.title]
          )
        }
      />
      <p className="text-danger">{gettext('This action cannot be undone!')}</p>

      {
        errors.non_field_errors?.map((error, index) => (
          <div key={index} className="text-danger mt-1">{error}</div>
        ))
      }
    </Modal>
  )
}

IntegrationDeleteModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  integration: PropTypes.object.isRequired
}

export default IntegrationDeleteModal
