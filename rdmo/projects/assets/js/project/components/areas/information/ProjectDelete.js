import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'
import Html from 'rdmo/core/assets/js/components/Html'

import { deleteProject } from '../../../actions/projectActions'

const ProjectDelete = () => {
  const dispatch = useDispatch()
  const { project } = useSelector((state) => state.project.project)

  const [showConfirm, setShowConfirm] = useState(false)

  const openConfirm = () => setShowConfirm(true)
  const closeConfirm = () => setShowConfirm(false)

  const handleDelete = () => {
    dispatch(deleteProject(project.id))
  }

  return (
    <div>
      <p className="mb-2">{gettext('This action cannot be undone. The project will be permanently removed!')}</p>

      <button className="btn btn-danger" onClick={openConfirm}>
        {gettext('Delete project')}
      </button>

      <Modal
        title={gettext('Delete project?')}
        show={showConfirm}
        onClose={closeConfirm}
        onSubmit={handleDelete}
        submitLabel={gettext('Delete')}
        submitProps={{className: 'btn btn-danger'}}
      >
        <Html html={interpolate(gettext(
          'Are you sure you want to delete the project <b>%s</b>?'), [project.title ?? '']
        )} />
        <p>
          {gettext('This action cannot be undone.')}
        </p>
      </Modal>
    </div>
  )
}

export default ProjectDelete
