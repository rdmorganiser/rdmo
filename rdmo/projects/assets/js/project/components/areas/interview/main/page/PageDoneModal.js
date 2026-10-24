import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import { Html, Modal } from 'rdmo/core/assets/js/components'

const PageDoneModal = ({ show, onClose, onSubmit }) => {
  const templates = useSelector((state) => state.templates)

  const submitLabel = (
    <span className="d-inline-flex align-items-center gap-2">
      {gettext('To Documents')} <i className="bi bi-arrow-right"></i>
    </span>
  )

  return (
    <Modal
      title={gettext('Done')}
      show={show}
      submitLabel={submitLabel}
      onClose={onClose}
      onSubmit={onSubmit}
      size="modal-lg"
    >
      <Html html={templates.project_interview_done} />
    </Modal>
  )
}

PageDoneModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
}

export default PageDoneModal
