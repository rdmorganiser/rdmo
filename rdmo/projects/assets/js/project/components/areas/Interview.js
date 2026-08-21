import React from 'react'
import { useSelector } from 'react-redux'
import { isNil } from 'lodash'

import InterviewMain from './interview/InterviewMain'
import InterviewOverview from './interview/InterviewOverview'

const Interview = () => {
  const config = useSelector((state) => state.config)

  return (
    <div className="project-interview">
      {
        isNil(config.pageId) ? (
          <InterviewOverview />
        ) : (
          <InterviewMain />
        )
      }
    </div>
  )
}

export default Interview
