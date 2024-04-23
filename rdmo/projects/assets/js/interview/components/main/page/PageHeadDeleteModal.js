import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

const PageHeadDeleteModal = ({ title, show, onClose, onSubmit }) => {
  return (
    <Modal title={title} show={show} submitText={gettext('Delete')} submitColor="danger"
           onClose={onClose} onSubmit={onSubmit}>
      <p>You are about to permanently delete this tab.</p>
      <p>This includes all given answers for this tab on all pages, not just this one.</p>
      <p className="text-danger">This action cannot be undone!</p>
    </Modal>
  )
}

PageHeadDeleteModal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
}

export default PageHeadDeleteModal
