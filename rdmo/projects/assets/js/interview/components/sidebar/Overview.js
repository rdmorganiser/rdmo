import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

import Template from 'rdmo/core/assets/js/components/Template'

const Overview = ({ overview, help }) => {

  const projectsUrl = `${baseUrl}/projects/`
  const projectUrl = `${baseUrl}/projects/${overview.id}`

  return (
    <>
      <h2>{gettext('Overview')}</h2>
      <Template template={help} />

      <div className="interview-overview">
        <ul className="list-unstyled">
          <li>
            {gettext('Project')}: <a href={projectUrl}>{overview.title}</a>
          </li>
          <li>
            {gettext('Catalog')}: {overview.catalog.title}
          </li>
        </ul>

        {
          overview.read_only && (
            <p>
              <span className="badge badge-read-only" title={gettext('You don\'t have write access to this project.')}>
                {gettext('read only')}
              </span>
            </p>
          )
        }

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
  overview: PropTypes.object.isRequired,
  help: PropTypes.string.isRequired
}

export default Overview
