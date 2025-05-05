import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { getUserRoles } from 'rdmo/projects/assets/js/common/utils'
import { deleteProject } from '../../actions/projectActions'

const ProjectDelete = () => {
  const dispatch = useDispatch()
  const currentUser = useSelector((state) => state.user.currentUser)
  const { project } = useSelector((state) => state.project.project)

  const handleDelete = () => {
    if (project?.id) {
      dispatch(deleteProject(project.id))
        .then(() => {
          window.location.href = '/projects/'
        })
        .catch((error) => {
          console.error('Failed to delete project:', error)
        })
    }
  }

  return (
    <div className="p-4 pb-3">
        <div className="mb-4">
          <div className="fw-bold mb-2">{gettext('Delete project')}</div>
          <div>{gettext('This action cannot be undone. The project will be permanently removed!')}</div>
        </div>
        <div className="text-end mt-2">
          <button className="element-button btn btn-xs btn-danger"
            disabled={!currentUser.is_superuser && !getUserRoles(project, currentUser.id, ['owners']).isProjectOwner}
            onClick={handleDelete}
          >
             {gettext('Delete project')}
          </button>
        </div>
      </div>
  )
}

export default ProjectDelete
