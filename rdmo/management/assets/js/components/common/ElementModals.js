import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Modal } from 'react-bootstrap';

const DeleteElementModal = ({ title, show, onClose, onDelete, children }) => {
  return (
    <Modal show={show} onHide={onClose} className="element-modal">
      <Modal.Header closeButton>
        <h2 className="modal-title">{title}</h2>
      </Modal.Header>
      <Modal.Body>
        { children }
      </Modal.Body>
      <Modal.Footer>
        <button type="button" className="btn btn-default" onClick={onClose}>
          {gettext('Close')}
        </button>
        <button type="button" className="btn btn-danger" onClick={onDelete}>
          {gettext('Delete')}
        </button>
      </Modal.Footer>
    </Modal>
  )
}

DeleteElementModal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export { DeleteElementModal }