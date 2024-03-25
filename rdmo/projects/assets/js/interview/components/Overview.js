import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

const Overview = ({ overview }) => {

  const projectsUrl = `${baseUrl}/projects/`
  const projectUrl = `${baseUrl}/projects/${overview.id}`

  return (
    <>
      <h2>{gettext('Overview')}</h2>

      <div className="interview-overview">
        <ul className="list-unstyled">
            <li>
                {gettext('Project')}: <a href={projectUrl}>{overview.title}</a>
            </li>
            <li>
                {/* TODO: get catalog title from catalog api */}
                {gettext('Catalog')}: {overview.catalog.title}
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
  overview: PropTypes.object.isRequired
}

export default Overview
