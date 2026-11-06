import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { Html, LinkButton, Tooltip } from 'rdmo/core/assets/js/components'

import { navigateDashboard } from '../../../actions/navigationActions'

import LocationLink from '../../helper/LocationLink'

const InterviewOverview = () => {
  const dispatch = useDispatch()
  const templates = useSelector((state) => state.templates)
  const navigation = useSelector((state) => state.project.navigation)
  const catalogHelp = useSelector((state) => state.project.project.project.catalog_help)
  const continuation = useSelector((state) => state.interview.continuation)

  const handleCardClick = (section) => dispatch(navigateDashboard({area: 'interview', pageId: section.first}))

  return navigation && (
    <div className="project-interview-overview">
      <div className="d-lg-flex justify-content-between align-items-center gap-5 mb-5">
        <h1 className="mb-lg-0 flex-grow-1">{gettext('Interview')}</h1>

        <LinkButton
          title={gettext('Import from parent project')}
          className="d-block"
          onClick={() => {}}
        >
          <i className="bi bi-upload me-1"></i> {gettext('Import from parent project')}
        </LinkButton>
        <LinkButton
          title={gettext('Import from uploaded file')}
          className="d-block"
          onClick={() => {}}
        >
          <i className="bi bi-upload me-1"></i> {gettext('Import from uploaded file')}
        </LinkButton>
      </div>

      {
        catalogHelp && (
          <div className="text-muted mb-4">
            <Html html={catalogHelp} />
          </div>
        )
      }

      {
        navigation.map((section, sectionIndex) => (
          <div key={section.id} className="d-flex align-items-center gap-4 mb-4">
            <div className="d-none d-md-block">
              {
                (section.count < section.total) ? (
                  <div className="circle border border-secondary text-secondary bg-white">
                    {sectionIndex + 1}
                  </div>
                ) : (
                  <div className="circle bg-primary text-white font-large">
                    <i className="bi bi-check-lg"></i>
                  </div>
                )
              }
            </div>

            <div
              className="card card-tile card-tile-border cursor-pointer flex-grow-1"
              onClick={() => handleCardClick(section)}
            >
              <div className="card-body d-flex flex-column">
                <div className="row">
                  <div className="col-md-8 ps-5">
                    <h3 className="mb-2">
                      <Html html={section.title} />
                    </h3>
                    {
                      !isEmpty(section.pages) && (
                        <ul className="list-unstyled font-small mb-0">
                          {
                            section.pages.map((page) => (
                              <li
                                key={page.id}
                                className={classNames({'continue': continuation && page.id == continuation.id})}
                              >
                                {
                                  page.show ? (
                                    <>
                                      <LocationLink
                                        title={page.title}
                                        location={{area: 'interview', pageId: page.id}}
                                      >
                                        <Html html={page.title} />
                                      </LocationLink>
                                    </>
                                  ) : (
                                    <span
                                      className="text-muted cursor-not-allowed"
                                      onClick={(event => event.stopPropagation())}
                                    >
                                      <Html html={page.title} />
                                    </span>
                                  )
                                }
                              </li>
                            ))
                          }
                        </ul>
                      )
                    }
                  </div>
                  <Tooltip title={<Html html={templates.project_interview_overview_count_tooltip} />} placement="top">
                    <div className="d-none d-md-block col-md-4">
                      <div className="row h-100">
                        <div className="col-md-6 border-start">
                          <div className="d-flex flex-column justify-content-center align-items-center h-100">
                            <p className="h3 text-center text-secondary">
                              {section.count}
                            </p>
                            <p className="h3 text-center text-secondary mb-0">
                              {gettext('Answers')}
                            </p>
                          </div>
                        </div>
                        <div className="col-md-6 border-start">
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
                  </Tooltip>
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
