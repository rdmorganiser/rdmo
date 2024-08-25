import React from 'react'
import PropTypes from 'prop-types'
import { Modal as BootstrapModal } from 'react-bootstrap'

const Modal = ({ title, show, modalProps, submitLabel, submitProps, onClose, onSubmit, children }) => {
  return (
    <BootstrapModal className="element-modal" onHide={onClose} show={show} {...modalProps}>
      <BootstrapModal.Header closeButton>
        <h2 className="modal-title">{title}</h2>
      </BootstrapModal.Header>
      {
        children && (
          <BootstrapModal.Body>
            { children }
          </BootstrapModal.Body>
        )
      }
      <BootstrapModal.Footer>
        <button type="button" className="btn btn-default" onClick={onClose}>
          {gettext('Close')}
        </button>
        {
          onSubmit && (
            <button type="button" className="btn btn-primary" onClick={onSubmit} {...submitProps}>
              {submitLabel ?? gettext('Save')}
            </button>
          )
        }
      </BootstrapModal.Footer>
    </BootstrapModal>
  )
}

Modal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  modalProps: PropTypes.object,
  submitLabel: PropTypes.string,
  submitProps: PropTypes.object,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node]).isRequired,
}

export default Modal
