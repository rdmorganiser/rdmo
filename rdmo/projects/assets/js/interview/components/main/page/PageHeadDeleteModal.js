import React from 'react'
import PropTypes from 'prop-types'

import Modal from 'rdmo/core/assets/js/components/Modal'

const PageHeadDeleteModal = ({ name, show, onClose, onSubmit }) => {
  return (
    <Modal title={gettext('Delete tab')} show={show} submitLabel={gettext('Delete')}
           submitProps={{className: 'btn btn-danger'}}
           onClose={onClose} onSubmit={onSubmit}>
      {
        name ? (
          <p dangerouslySetInnerHTML={{
          __html: interpolate(gettext('You are about to permanently delete the tab named: <strong>%s</strong>'), [name])
          }}></p>
        ) : (
          <p>{gettext('You are about to permanently delete this tab.')}</p>
        )
      }
      <p>{gettext('This includes all given answers for this tab on all pages, not just this one.')}</p>
      <p className="text-danger">{gettext('This action cannot be undone!')}</p>
    </Modal>
  )
}

PageHeadDeleteModal.propTypes = {
  name: PropTypes.string,
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
}

export default PageHeadDeleteModal
