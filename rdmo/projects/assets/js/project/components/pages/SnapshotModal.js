import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import { Input, Textarea } from 'rdmo/core/assets/js/components/forms'
import { Modal } from 'rdmo/core/assets/js/_bs53/components'

import {
  createSnapshot,
  updateSnapshot,
  clearProjectErrors
} from '../../actions/projectActions'
import { useFieldErrors } from '../../hooks/useFieldErrors'

const initialForm = { title: '', description: '' }

const SnapshotModal = ({ show, onClose, snapshot }) => {
  const templates = useSelector((state) => state.templates)
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
        <Input
          id="snapshot-title"
          type="text"
          className="mt-2"
          label={gettext('Title')}
          name="title"
          required
          value={formData.title}
          onChange={(e) => setField('title', e.target.value)}
        />
        <Textarea
          id="snapshot-description"
          className="mt-2"
          help={<Html html={templates.project_view_snapshot_description_help} />}
          label={gettext('Description')}
          name="description"
          value={formData.description}
          onChange={(e) => setField('description', e.target.value)}
          rows={4}
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
