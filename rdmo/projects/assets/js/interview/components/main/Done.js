import React from 'react'
import PropTypes from 'prop-types'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { projectId }  from '../../utils/meta'

import Html from 'rdmo/core/assets/js/components/Html'

const Done = ({ templates }) => {

  const projectUrl = `${baseUrl}/projects/${projectId}/`
  const answersUrl = `${baseUrl}/projects/${projectId}/answers/`

  return (
    <>
      <Html html={templates.project_interview_done} />

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
  templates: PropTypes.object.isRequired
}

export default Done
