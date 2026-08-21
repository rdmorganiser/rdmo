import React from 'react'
import { useSelector } from 'react-redux'
import { isNil } from 'lodash'

import InterviewOverview from './interview/InterviewOverview'
import InterviewPage from './interview/InterviewPage'

const Interview = () => {
  const config = useSelector((state) => state.config)

  return (
    <div className="project-interview">
      <h1>{gettext('Interview')}</h1>

      {
        isNil(config.pageId) ? (
          <InterviewOverview />
        ) : (
          <InterviewPage />
        )
      }
    </div>
  )
}

export default Interview
