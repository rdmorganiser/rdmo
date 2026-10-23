import React from 'react'
import { useSelector } from 'react-redux'
import classNames from 'classnames'

import Html from 'rdmo/core/assets/js/components/Html'

import NavigationLink from './NavigationLink'

const Navigation = () => {
  const { page: currentPage } = useSelector((state) => state.interview)
  const navigation = useSelector((state) => state.project.navigation)
  const templates = useSelector((state) => state.templates)

  return currentPage && navigation && (
    <>
      <h3>{gettext('Navigation')}</h3>
      <Html html={templates?.project_interview_navigation_help} />

      <div className="project-interview-navigation">
        <ul className="list-unstyled">
          {
            navigation.map((section, sectionIndex) => (
              <li key={sectionIndex}>
                <NavigationLink element={section} />
                {
                  (section.id === currentPage.section.id) && (
                    <ul className="list-unstyled">
                      {
                        section.pages.map((page, pageIndex) => (
                          <li
                            key={pageIndex}
                            className={classNames('ps-4', {'active': currentPage ? page.id == currentPage.id : false})}
                          >
                            <NavigationLink element={page} />
                          </li>
                        ))
                      }
                    </ul>
                  )
                }
              </li>
            ))
          }
        </ul>
      </div>
    </>
  )
}

export default Navigation
