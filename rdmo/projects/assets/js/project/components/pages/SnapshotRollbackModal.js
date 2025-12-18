import React from 'react'
import PropTypes from 'prop-types'
// import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

// import { rollbackSnapshot } from '../../actions/projectActions'
import { useFieldErrors } from '../../hooks/useFieldErrors'

const SnapshotRollbackModal = ({ show, onClose, snapshot }) => {
  // const dispatch = useDispatch()
  // const { project } = useSelector((state) => state.project.project) ?? {}
  const errors = useFieldErrors()
  const handleSubmit = () => {
    console.log('rolling back snapshot')
  }

  return (
    <Modal
      title={gettext('Roll back to snapshot')}
      show={show}
      onClose={onClose}
      onSubmit={handleSubmit}
      submitLabel={gettext('Roll back')}
      submitProps={{ className: 'btn btn-danger' }}
      size="modal-lg"
    >
      <Html
        html={
          interpolate(
            gettext('You are about to roll back all values to the snapshot <b>%s</b>.'), [snapshot?.title]) +
          '<br>' +
          gettext('All newer changes will be permanently discarded.') +
          '<br><br>' +
          gettext('This action cannot be undone!')
        }
      />
      {errors.non_field_errors?.map((err, i) => (
        <div key={i} className="text-danger mt-1">{err}</div>
      ))}
    </Modal>
  )
}

SnapshotRollbackModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  snapshot: PropTypes.object,
}

export default SnapshotRollbackModal
