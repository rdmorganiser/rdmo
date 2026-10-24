import React from 'react'
import { useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

const InterviewErrors = () => {
  const templates = useSelector((state) => state.templates)
  const errors = useSelector((state) => state.interview.errors)

  return (
    <>
      <Html html={templates.project_interview_error} />

      <ul className="well list-unstyled text-danger">
        {
          errors.map((error, errorIndex) => (
            <li key={errorIndex}>
              {error.actionType}
              {error.statusText && <>: {error.statusText}</>}
              {error.status && <>({error.status})</>}
            </li>
          ))
        }
      </ul>

      <p>
        <a href="#" onClick={() => window.location.reload()}>{gettext('Reload page')}</a>
      </p>
    </>
  )
}

export default InterviewErrors
