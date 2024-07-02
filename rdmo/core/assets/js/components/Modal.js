import React from 'react'
import PropTypes from 'prop-types'
import { Modal as BootstrapModal } from 'react-bootstrap'

const Modal = ({ bsSize, buttonLabel, buttonProps, title, show, onClose, onSave, children }) => {
  return (
    <BootstrapModal bsSize={bsSize} className="element-modal" onHide={onClose} show={show}>
      <BootstrapModal.Header closeButton>
        <h2 className="modal-title">{title}</h2>
      </BootstrapModal.Header>
      <BootstrapModal.Body>
        { children }
      </BootstrapModal.Body>
      <BootstrapModal.Footer>
        <button type="button" className="btn btn-default" onClick={onClose}>
          {gettext('Close')}
        </button>
        { onSave ?
          <button type="button" className="btn btn-primary" onClick={onSave} {...buttonProps}>
            {buttonLabel ?? gettext('Save')}
          </button>
          : null
        }
      </BootstrapModal.Footer>
    </BootstrapModal>
  )
}

Modal.propTypes = {
  bsSize: PropTypes.oneOf(['lg', 'large', 'sm', 'small']),
  buttonLabel: PropTypes.string,
  buttonProps: PropTypes.object,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node]).isRequired,
  onClose: PropTypes.func.isRequired,
  onSave: PropTypes.func,
  show: PropTypes.bool.isRequired,
  title: PropTypes.string.isRequired,
}

export default Modal
