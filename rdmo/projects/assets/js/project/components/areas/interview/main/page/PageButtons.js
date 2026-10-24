import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { showDone } from '../../../../../actions/interviewActions'
import { navigateDashboard } from '../../../../../actions/navigationActions'

const PageButtons = () => {
  const dispatch = useDispatch()
  const page = useSelector((state) => state.interview.page)

  return (
    <div className="project-interview-page-buttons">
      <div className="d-flex">
        {
          page.prev_page && (
            <button
              type="button"
              onClick={() => dispatch(navigateDashboard({ area: 'interview', pageId: page.prev_page}, true))}
              disabled={!page.prev_page}
              className="btn btn-outline-primary"
            >
              {gettext('Back')}
            </button>
          )
        }
        {
          page.next_page ? (
            <button
              type="button"
              onClick={() => dispatch(navigateDashboard({ area: 'interview', pageId: page.next_page}))}
              className="btn btn-primary ms-auto"
            >
              {gettext('Proceed')}
            </button>
          ) : (
            <button
              type="button"
              onClick={() => dispatch(showDone())}
              className="btn btn-primary ms-auto"
            >
              {gettext('Complete questionnaire')}
            </button>
          )
        }
      </div>
    </div>
  )
}

export default PageButtons
