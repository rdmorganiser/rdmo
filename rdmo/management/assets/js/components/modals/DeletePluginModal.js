import React from 'react'
import PropTypes from 'prop-types'

import { Modal } from 'react-bootstrap'

const DeletePluginModal = ({ plugin, info, show, onClose, onDelete }) => (
  <Modal className="delete-modal" bsSize="large" show={show} onHide={onClose}>
    <Modal.Header closeButton>
      <Modal.Title>{gettext('Delete plugin')}</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <p dangerouslySetInnerHTML={{__html: interpolate(
        gettext('Do you really want to delete the plugin <code>%(plugin)s</code>?'),
        {plugin: plugin.uri}
      )}} />
      { info }
    </Modal.Body>
    <Modal.Footer>
      <button className="btn btn-default" onClick={onClose}>{gettext('Cancel')}</button>
      <button className="btn btn-danger" onClick={onDelete}>{gettext('Delete plugin')}</button>
    </Modal.Footer>
  </Modal>
)

DeletePluginModal.propTypes = {
  plugin: PropTypes.object.isRequired,
  info: PropTypes.object,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired
}

export default DeletePluginModal
