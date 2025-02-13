import React from 'react'

import { Tile } from 'rdmo/core/assets/js/components'
import ProjectForm from './ProjectForm'

const ProjectData = () => {
  return (
    // <>
    //   <Tile title="Projektdaten" size="fullWidth">
    //     <ProjectForm />
    //   </Tile>
    //   <div className="d-flex flex-wrap gap-3">
    //   <Tile size="compact">
    //     {'Delete project'}
    //   </Tile>
    // </>

    <div className="container-fluid px-3">
    <div className="row g-3">
      <Tile title="Projektdaten" size="fullWidth">
        <ProjectForm />
      </Tile>
    </div>

    <div className="row g-3">
      <Tile size="fullWidth">
        Delete project
      </Tile>
    </div>
  </div>

  )
}

export default ProjectData
