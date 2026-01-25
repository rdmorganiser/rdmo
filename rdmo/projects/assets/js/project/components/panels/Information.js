import React from 'react'
import { useSelector } from 'react-redux'

import HierarchyTree from './information/HierarchyTree'
import ProjectForm from './information/ProjectForm'
import ProjectDelete from './information/ProjectDelete'

const Information = () => {
  const { hierarchy, project } = useSelector((state) => state.project.project) ?? {}
  const perms = project?.permissions ?? {}

  return (
    <div className="project-information">
      <h1 className="mb-5">{gettext('Project information')}</h1>

      <div className="card card-tile mb-4">
        <div className="card-body">
          <ProjectForm disabled={!perms.can_change_project} />
        </div>
      </div>

      <div className="card card-tile mb-4">
        <div className="card-body">
          <h3>{gettext('Project hierarchy')}</h3>
          <HierarchyTree hierarchy={hierarchy} />
        </div>
      </div>

      {
        perms.can_delete_project && (
          <div className="card card-tile mb-4">
            <div className="card-body">
              <h3>{gettext('Delete project')}</h3>
              <ProjectDelete />
            </div>
          </div>
        )
      }
    </div>
  )
}

export default Information
