import React from 'react'
import { useSelector } from 'react-redux'
import { isNil } from 'lodash'

import { Tile } from '../helper'
import ProjectForm from './ProjectForm'
import ProjectDelete from './ProjectDelete'
import { getUserRoles, userIsManager } from 'rdmo/projects/assets/js/common/utils'

const ProjectData = () => {
  const project = useSelector((state) => state.project)
  const user = useSelector((state) => state.user)

  if (isNil(project.project) || isNil(user.currentUser)) {
    return
  }

  const allowed = userIsManager(user.currentUser) ||
                  getUserRoles(project.project.project, user.currentUser.id, ['owners']).isProjectOwner

  return (
    <div className="container-fluid px-3">
    <div className="row g-3">
      <Tile title={gettext('Project data')} size="fullWidth">
        <ProjectForm />
      </Tile>
    </div>

    {allowed && (
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
