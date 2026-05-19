import React from 'react'
import { useSelector } from 'react-redux'

import CopyProject from './information/CopyProject'
import HierarchyTree from './information/HierarchyTree'
import ProjectDelete from './information/ProjectDelete'
import ProjectForm from './information/ProjectForm'
import ProjectVisibilityForm from './information/ProjectVisibilityForm'

const Information = () => {
  const { hierarchy, project } = useSelector((state) => state.project.project) ?? {}
  const perms = project?.permissions ?? {}

  return (
    <div className="project-information">
      <div className="d-lg-flex justify-content-between align-items-center mb-5">
        <h1 className="mb-lg-0">{gettext('Project information')}</h1>
        <CopyProject project={project} />
      </div>


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
        perms.can_view_visibility && (
          <div className="card card-tile mb-4">
            <div className="card-body">
              <ProjectVisibilityForm projectId={project.id} />
            </div>
          </div>
        )
      }

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
