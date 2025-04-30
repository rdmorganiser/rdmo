import React from 'react'
import { useSelector } from 'react-redux'
import { DeleteButton } from 'rdmo/management/assets/js/components/common/Buttons.js'
import { getUserRoles } from 'rdmo/projects/assets/js/common/utils'

const ProjectDelete = () => {
  const currentUser = useSelector((state) => state.user.currentUser)
  const { project } = useSelector((state) => state.project.project)

  const handleDelete = () => {
    // Insert deletion logic here
    console.log('Deleting project:', project.title)
  }

  return (
    <div className="p-4 pb-3">
        <div className="mb-4">
          <div className="fw-bold mb-2">Projekt löschen</div>
          <div>Diese Aktion kann nicht rückgängig gemacht werden, das Projekt wird permanent entfernt!</div>
        </div>
        <div className="text-end mt-2">
          <DeleteButton
              disabled={!currentUser.is_superuser && !getUserRoles(project, currentUser.id, ['owners']).isProjectOwner}
              onClick={handleDelete}
          >
            Entfernen
          </DeleteButton>
        </div>
      </div>
  )
}

export default ProjectDelete
