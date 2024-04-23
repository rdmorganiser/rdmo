import React from 'react'
import PropTypes from 'prop-types'
import { Modal as BootstrapModal } from 'react-bootstrap'

const Modal = ({ title, show, bsSize, submitText, submitColor, disableSubmit,
                 onClose, onSubmit, children }) => {
  return (
    <BootstrapModal bsSize={bsSize} show={show} onHide={onClose}>
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
        <button type="button" className={`btn btn-${submitColor}`} disabled={disableSubmit} onClick={onSubmit}>
          {submitText}
        </button>
      </BootstrapModal.Footer>
    </BootstrapModal>
  )
}

Modal.defaultProps = {
  submitText: gettext('Save'),
  submitColor: 'primary',
  disableSubmit: false
}

Modal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  bsSize: PropTypes.string,
  submitText: PropTypes.string,
  submitColor: PropTypes.string,
  disableSubmit: PropTypes.bool,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default Modal
