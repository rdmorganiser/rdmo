import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import Modal from 'rdmo/core/assets/js/components/Modal'

import { deleteSnapshot } from '../../../actions/projectActions'
import { useFieldErrors } from '../../../hooks/useFieldErrors'

const SnapshotDeleteModal = ({ show, onClose, snapshot }) => {
  const dispatch = useDispatch()
  const errors = useFieldErrors()
  const handleSubmit = () => {
    try {
      dispatch(deleteSnapshot(snapshot.id))
      onClose()
    } catch {
      // keep modal open; errors are shown via useFieldErrors
    }
  }

  return (
    <Modal
      title={gettext('Delete snapshot')}
      show={show}
      onClose={onClose}
      onSubmit={handleSubmit}
      submitLabel={gettext('Delete')}
      submitProps={{ className: 'btn btn-danger' }}
      size="modal-lg"
    >
      <Html
        html={
          `<p>${interpolate(
            gettext('You are about to delete snapshot <b>%s</b>.'),
            [snapshot?.title]
          )
          }</p>`
        }
      />
      {
        errors.non_field_errors?.map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))
      }
    </Modal>
  )
}

SnapshotDeleteModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  snapshot: PropTypes.object,
}

export default SnapshotDeleteModal
