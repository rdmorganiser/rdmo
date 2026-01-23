import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { get, isNil } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { Link } from 'rdmo/core/assets/js/components'

import { HierarchyTree, Tile } from '../helper'

import ProjectForm from './information/ProjectForm'
import ProjectDelete from './information/ProjectDelete'

const ProjectData = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const { hierarchy, project } = useSelector((state) => state.project.project) ?? {}
  const user = useSelector((state) => state.user)
  const perms = project?.permissions ?? {}

  const showHierarchy = isTruthy(get(config, 'showHierarchy', false))
  const toggleHierarchy = () => dispatch(updateConfig('showHierarchy', !showHierarchy))

  if (isNil(project) || isNil(user.currentUser)) {
    return
  }

  return (
    <div className="project-information">
      <h1 className="mb-5">{gettext('Project information')}</h1>

      <div className="row g-3">
        <Link className="element-link mb-10" onClick={toggleHierarchy}>
          {showHierarchy ? gettext('Hide project hierarchy') : gettext('Show project hierarchy')}
        </Link>
        {showHierarchy &&
        <Tile title={gettext('Project hierarchy')} size="fullWidth">
          <HierarchyTree hierarchy={hierarchy} />
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
