import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

import Template from 'rdmo/core/assets/js/components/Template'

import projectId from '../../utils/projectId'

const Errors = ({ templates, errors }) => {
  const projectUrl = `${baseUrl}/projects/${projectId}/`

  return (
    <>
      <Template template={templates.project_interview_error} />

      <ul className="well list-unstyled text-danger">
        {
          errors.map((error, errorIndex) => (
            <li key={errorIndex}>{error.actionType}: {error.statusText} ({error.status})</li>
          ))
        }
      </ul>

      <p>
        <a href="#" onClick={() => window.location.reload()}>{gettext('Reload page')}</a>
      </p>
      <p>
        <a href={projectUrl}>{gettext('Back to project overview')}</a>
      </p>
    </>
  )
}

Errors.propTypes = {
  templates: PropTypes.object.isRequired,
  errors: PropTypes.array.isRequired
}

export default Errors
