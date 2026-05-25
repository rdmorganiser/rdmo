import React, { useState } from 'react'
import { useSelector } from 'react-redux'

import ProjectDeleteModal from './ProjectDeleteModal'
const ProjectDelete = () => {
  const { project } = useSelector((state) => state.project.project)

  const [showConfirm, setShowConfirm] = useState(false)

  const openConfirm = () => setShowConfirm(true)
  const closeConfirm = () => setShowConfirm(false)

  return (
    <div>
      <p className="mb-2">
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

export default ProjectDelete
