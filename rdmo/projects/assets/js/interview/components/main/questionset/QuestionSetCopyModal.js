import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

const QuestionSetCopyModal = ({ title, show, onClose, onSubmit }) => {
  return (
    <Modal title={title} show={show} submitText={gettext('Copy')} submitColor="info"
           onClose={onClose} onSubmit={onSubmit}>
    </Modal>
  )
}

QuestionSetCopyModal.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
}

export default QuestionSetCopyModal
