import React from 'react'
import PropTypes from 'prop-types'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import Html from 'rdmo/core/assets/js/components/Html'

const Overview = ({ config, overview, help, configActions }) => {

  const isManager = (overview.is_superuser || overview.is_editor || overview.is_reviewer)

  const projectsUrl = `${baseUrl}/projects/`
  const projectUrl = `${baseUrl}/projects/${overview.id}`

  const toggleManagement = () => {
    configActions.updateConfig('showManagement', !config.showManagement)
  }

  return (
    <>
      <h2>{gettext('Overview')}</h2>
      <Html html={help} />

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
          isManager && (
            <ul className="list-unstyled">
              <li>
                <button role="button" className="btn btn-link" onClick={toggleManagement}>
                  {config.showManagement ? gettext('Hide management panels') : gettext('Show management panels')}
                </button>
              </li>
            </ul>
          )
        }

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
  config: PropTypes.object.isRequired,
  overview: PropTypes.object.isRequired,
  help: PropTypes.string.isRequired,
  configActions: PropTypes.object.isRequired
}

export default Overview
