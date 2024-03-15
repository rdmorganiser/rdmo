import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

const Overview = ({ project }) => {

  const projectsUrl = `${baseUrl}/projects/`
  const projectUrl = `${baseUrl}/projects/${project.id}`

  return (
    <>
      <h2>{gettext('Overview')}</h2>

      <div className="interview-overview">
        <ul className="list-unstyled">
            <li>
                {gettext('Project')}: <a href={projectUrl}>{project.title}</a>
            </li>
            <li>
                {/* TODO: get catalog title from catalog api */}
                {gettext('Catalog')}: {project.catalog}
            </li>
        </ul>

        <ul className="list-unstyled">
            <li>
                <a href="#" onClick={() => window.location.reload()}>{gettext('Reload page')}</a>
            </li>
            <li>
                <a href={projectsUrl}>{gettext('Back to my projects')}</a>
            </li>
        </ul>
      </div>
    </>
  )
}

Overview.propTypes = {
  project: PropTypes.object.isRequired
}

export default Overview
