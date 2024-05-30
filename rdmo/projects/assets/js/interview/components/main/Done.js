import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

import projectId from '../../utils/projectId'

import Template from 'rdmo/core/assets/js/components/Template'

const Done = ({ templates }) => {

  const projectUrl = `${baseUrl}/projects/${projectId}/`
  const answersUrl = `${baseUrl}/projects/${projectId}/answers/`

  return (
    <>
      <Template template={templates.project_interview_done} />

      <p>
        <a href={answersUrl}>{gettext('View answers')}</a>
      </p>

      <p>
        <a href={projectUrl}>{gettext('Back to project overview')}</a>
      </p>
    </>
  )
}

Done.propTypes = {
  templates: PropTypes.object.isRequired,
  overview: PropTypes.object.isRequired
}

export default Done
