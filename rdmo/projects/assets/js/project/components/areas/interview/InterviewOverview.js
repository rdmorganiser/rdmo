import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

import LocationLink from '../../helper/LocationLink'

const InterviewOverview = () => {
  const { navigation } = useSelector((state) => state.project)

  return navigation && (
    <div className="project-interview-overview">
      <h2>{gettext('Interview')}</h2>

      {
        navigation.map((section) => (
          <div key={section.id} className="card card-tile mb-4 rounded-3">
            <div className="card-body d-flex flex-column">
              <div className="row">
                <div className="col-md-8">
                  <h2>
                    <Html html={section.title} />
                  </h2>
                  {
                    !isEmpty(section.pages) && (
                      <ul className="mb-0 text-secondary">
                        {
                          section.pages.map((page) => (
                            <li key={page.id}>
                              <LocationLink
                                title={page.title}
                                location={{area: 'interview', pageId: page.id}}
                              >
                                <Html html={page.title} />
                              </LocationLink>
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
