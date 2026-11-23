import React from 'react'
import { useSelector } from 'react-redux'
import { isNil } from 'lodash'

import InterviewDone from './interview/InterviewDone'
import InterviewMain from './interview/InterviewMain'
import InterviewOverview from './interview/InterviewOverview'

const Interview = () => {
  const { pageId } = useSelector((state) => state.location)

  return (
    <div className="project-interview">
      {
        isNil(pageId) ? (
          <InterviewOverview />
        ) : (
          <InterviewMain />
        )
      }
      <InterviewDone />
    </div>
  )
}

export default Interview
