import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'

import {
  createSnapshot,
  updateSnapshot,
  clearProjectErrors
} from '../../actions/projectActions'
import { useFieldErrors } from '../../hooks/useFieldErrors'

const initialForm = { title: '', description: '' }

const SnapshotModal = ({ show, onClose, snapshot }) => {
  const dispatch = useDispatch()
  const errors = useFieldErrors()

  const [formData, setFormData] = useState(initialForm)

  const isEdit = !!(snapshot && snapshot.id)
  const formId = isEdit ? 'update-snapshot-form' : 'create-snapshot-form'

  useEffect(() => {
    if (show) {
      if (isEdit) {
        setFormData({
          title: snapshot.title,
          description: snapshot.description
        })
      } else {
        setFormData(initialForm)
      }
      dispatch(clearProjectErrors())
    }
  }, [show, snapshot, dispatch])

  const setField = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    try {
      if (snapshot && snapshot.id) {
        dispatch(updateSnapshot(snapshot.id, formData))
      } else {
        dispatch(createSnapshot(formData))
      }
      onClose()
    } catch {
      // keep modal open; errors are shown via useFieldErrors
    }
  }

  return (
    <Modal
      title={isEdit ? gettext('Update snapshot') : gettext('Create new snapshot')}
      show={show}
      onClose={onClose}
      onSubmit={() => { }} // render the Modal's submit button
      submitLabel={isEdit ? gettext('Update snapshot') : gettext('Create snapshot')}
      submitProps={{ type: 'submit', form: formId }}
      size="modal-lg"
    >
      <form id={formId} onSubmit={handleSubmit}>
        <label className="form-label fw-bold" htmlFor="snapshot-title">
          {gettext('Title')}
        </label>
        <div>{gettext('The title for this snapshot.')}</div>
        <input
          id="snapshot-title"
          type="text"
          className="form-control mt-2"
          name="title"
          required
          value={formData.title}
          onChange={(e) => setField('title', e.target.value)}
        />

        <label className="form-label fw-bold" htmlFor="snapshot-description">
          {gettext('Description')}
        </label>
        <div>{gettext('The description for this snapshot.')}</div>
        <input
          id="snapshot-description"
          type="text"
          className="form-control mt-2"
          name="description"
          value={formData.description}
          onChange={(e) => setField('description', e.target.value)}
        />

        {errors.non_field_errors?.map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))}
      </form>
    </Modal>
  )
}

SnapshotModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  snapshot: PropTypes.object,
}

export default SnapshotModal
