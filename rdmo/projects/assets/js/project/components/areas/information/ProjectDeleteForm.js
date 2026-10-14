import React, { useState } from 'react'
import { useSelector } from 'react-redux'

import ProjectDeleteModal from './ProjectDeleteModal'

const ProjectDeleteForm = () => {
  const { project } = useSelector((state) => state.project.project)

  const [showConfirm, setShowConfirm] = useState(false)

  const openConfirm = () => setShowConfirm(true)
  const closeConfirm = () => setShowConfirm(false)

  return (
    <div>
      <h3 className="mb-2">{gettext('Delete project')}</h3>

      <p className="form-text mb-3">
        {gettext('This action cannot be undone. The project will be permanently removed!')}
      </p>

      <button className="btn btn-danger" onClick={openConfirm}>
        {gettext('Delete project')}
      </button>

      <ProjectDeleteModal
        project={project}
        show={showConfirm}
        onClose={closeConfirm}
      />
    </div>
  )
}

export default ProjectDeleteForm
