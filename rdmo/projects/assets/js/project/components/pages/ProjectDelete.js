import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { deleteProject } from '../../actions/projectActions'
import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

const ProjectDelete = () => {
  const dispatch = useDispatch()
  const { project } = useSelector((state) => state.project.project)

  const [showConfirm, setShowConfirm] = useState(false)

  const openConfirm = () => setShowConfirm(true)
  const closeConfirm = () => setShowConfirm(false)

  const handleDelete = () => {
    if (!project?.id) return
    dispatch(deleteProject(project.id))
      .then(() => {
        window.location.href = '/projects/'
      })
      .catch((error) => {
        console.error('Failed to delete project:', error)
      })
      .finally(() => {
        setShowConfirm(false)
      })
  }

  return (
    <div className="p-4 pb-3">
      <div className="mb-4">
        <div className="fw-bold mb-2">{gettext('Delete project')}</div>
        <div>{gettext('This action cannot be undone. The project will be permanently removed!')}</div>
      </div>

      <div className="text-end mt-2">
        <button
          className="element-button btn btn-xs btn-danger"
          onClick={openConfirm}
        >
          {gettext('Delete project')}
        </button>
      </div>

      <Modal
        title={gettext('Delete project?')}
        show={showConfirm}
        onClose={closeConfirm}
        onSubmit={handleDelete}
        submitLabel={gettext('Delete')}
        submitProps={{
          className: 'btn btn-danger',
          'data-testid': 'confirm-delete-button'
        }}
        size=""
      >
        <p className="mb-0">
          {interpolate(gettext('Are you sure you want to delete the project "%s"?'), [project?.title ?? ''])}
          <br />
          {gettext('This action cannot be undone.')}
        </p>
      </Modal>
    </div>
  )
}

export default ProjectDelete
