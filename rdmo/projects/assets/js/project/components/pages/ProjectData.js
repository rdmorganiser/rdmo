import React from 'react'

import { Tile } from '../helper'
import ProjectForm from './ProjectForm'
import ProjectDelete from './ProjectDelete'

const ProjectData = () => {
  return (

    <div className="container-fluid px-3">
    <div className="row g-3">
      <Tile title={gettext('Project data')} size="fullWidth">
        <ProjectForm />
      </Tile>
    </div>

    <div className="row g-3">
      <Tile size="fullWidth" style="warning">
        <ProjectDelete />
      </Tile>
    </div>
  </div>

  )
}

export default ProjectData
