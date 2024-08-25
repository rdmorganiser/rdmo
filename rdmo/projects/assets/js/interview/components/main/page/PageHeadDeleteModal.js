import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

const PageHeadDeleteModal = ({ title, show, onClose, onSubmit }) => {
  return (
    <Modal title={title} show={show} submitLabel={gettext('Delete')} submitProps={{className: 'btn btn-danger'}}
           onClose={onClose} onSubmit={onSubmit}>
      <p>{gettext('You are about to permanently delete this tab.')}</p>
      <p>{gettext('This includes all given answers for this tab on all pages, not just this one.')}</p>
      <p className="text-danger">{gettext('This action cannot be undone!')}</p>
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
