import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty, isNil } from 'lodash'

import InterviewDone from './interview/InterviewDone'
import InterviewErrors from './interview/InterviewErrors'
import InterviewMain from './interview/InterviewMain'
import InterviewOverview from './interview/InterviewOverview'

const Interview = () => {
  const config = useSelector((state) => state.config)
  const errors = useSelector((state) => state.interview.errors)

  if (!isEmpty(errors)) {
    return (
      <InterviewErrors />
    )
  }

  return (
    <div className="project-interview">
      {
        isNil(config.pageId) ? (
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
