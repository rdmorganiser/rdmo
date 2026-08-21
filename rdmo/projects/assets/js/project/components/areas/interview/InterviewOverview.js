import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { navigateDashboard } from '../../../actions/navigationActions'

const InterviewOverview = () => {
  const dispatch = useDispatch()

  const { navigation } = useSelector((state) => state.project) ?? {}

  return navigation && (
    <div className="project-interview-overview">
      {
        navigation.map((section) => (
          <div key={section.id} className="card card-tile mb-4 rounded-3">
            <div className="card-body d-flex flex-column">
              <div className="row">
                <div className="col-md-8">
                  <h2>{section.title}</h2>
                  {
                    !isEmpty(section.pages) && (
                      <ul className="mb-0 text-secondary">
                        {
                          section.pages.map((page) => (
                            <li key={page.id}>
                              <button
                                className="link"
                                onClick={() => dispatch(navigateDashboard({area: 'interview', pageId: page.id}))}
                              >
                                {page.title}
                              </button>
                            </li>
                          ))
                        }
                      </ul>
                    )
                  }
                </div>
                <div className="col-md-2 border-start">
                  <div className="d-flex flex-column justify-content-center align-items-center h-100">
                    <p className="h3 text-center text-secondary">
                      {section.count}
                    </p>
                    <p className="h3 text-center text-secondary mb-0">
                      {gettext('Answers')}
                    </p>
                  </div>
                </div>
                <div className="col-md-2 border-start">
                  <div className="d-flex flex-column justify-content-center align-items-center h-100">
                    <p className="h3 text-center text-secondary">
                      {section.total}
                    </p>
                    <p className="h3 text-center text-secondary mb-0">
                      {gettext('Questions')}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))
      }
    </div>
  )
}

export default InterviewOverview
