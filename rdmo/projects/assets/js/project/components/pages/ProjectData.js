import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { get, isNil } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { Link } from 'rdmo/core/assets/js/components'
import { HierarchyTree, Tile } from '../helper'
import ProjectForm from './ProjectForm'
import ProjectDelete from './ProjectDelete'

const ProjectData = () => {
  const config = useSelector((state) => state.config)
  const { perms, project } = useSelector((state) => state.project)
  const user = useSelector((state) => state.user)
  const dispatch = useDispatch()

  const showHierarchy = String(get(config, 'showHierarchy', false)) === 'true'
  const toggleHierarchy = () => dispatch(updateConfig('showHierarchy', !showHierarchy))

  if (isNil(project) || isNil(user.currentUser)) {
    return
  }

  return (
      <div className="container-fluid px-3">
        <div className="row g-3">
          <Link className="element-link mb-10" onClick={toggleHierarchy}>
            {showHierarchy ? gettext('Hide project hierarchy') : gettext('Show project hierarchy')}
          </Link>
          { showHierarchy &&
          <Tile title={gettext('Project hierarchy')} size="fullWidth">
            <HierarchyTree hierarchy={project.hierarchy} />
          </Tile>
          }
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
