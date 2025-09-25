import React from 'react'
import { useSelector } from 'react-redux'
import { isNil } from 'lodash'

import { Tile } from '../helper'
import ProjectForm from './ProjectForm'
import ProjectDelete from './ProjectDelete'

const ProjectData = () => {
  const { perms, project } = useSelector((state) => state.project)
  const user = useSelector((state) => state.user)

  if (isNil(project) || isNil(user.currentUser)) {
    return
  }

  return (
    <div className="container-fluid px-3">
    <div className="row g-3">
      <Tile title={gettext('Project data')} size="fullWidth">
        <ProjectForm disabled={!perms.can_change_project} />
      </Tile>
    </div>

    {perms.can_delete_project && (
        <div className="row g-3">
          <Tile size="fullWidth" style="warning">
            <ProjectDelete />
          </Tile>
        </div>
    )}
  </div>

  )
}

export default ProjectData
