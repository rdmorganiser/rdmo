import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

const QuestionSetDeleteModal = ({ title, show, onClose, onSubmit }) => {
  return (
    <Modal title={title} show={show} submitText={gettext('Delete')} submitColor="danger"
           onClose={onClose} onSubmit={onSubmit}>
      <p>{gettext('You are about to permanently delete this block.')}</p>
      <p className="text-danger">{gettext('This action cannot be undone!')}</p>
    </Modal>
  )
}

QuestionSetDeleteModal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
}

export default QuestionSetDeleteModal
