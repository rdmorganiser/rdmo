import React from 'react'
import { useSelector } from 'react-redux'
import classNames from 'classnames'

import Html from 'rdmo/core/assets/js/components/Html'

import NavigationLink from './NavigationLink'

const Navigation = () => {
  const { pageId: currentPageId } = useSelector((state) => state.config)
  const navigation = useSelector((state) => state.project.navigation)
  const templates = useSelector((state) => state.templates)

  const currentSection = {
    id: 1
  }

  return navigation && (
    <>
      <h3>{gettext('Navigation')}</h3>
      <Html html={templates?.project_interview_navigation_help} />

      <ul className="list-unstyled">
        {
          navigation.map((section, sectionIndex) => (
            <li key={sectionIndex}>
              <NavigationLink element={section} />
              {
                (section.id === currentSection?.id) && (
                  <ul className="list-unstyled">
                    {
                      section.pages.map((page, pageIndex) => (
                        <li key={pageIndex} className={classNames('ps-4', {'active': page.id === currentPageId})}>
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
    </>
  )
}

export default Navigation
