import React from 'react'
import { useSelector } from 'react-redux'
import classNames from 'classnames'

import Html from 'rdmo/core/assets/js/components/Html'

import Link from '../../../helper/Link'

const Navigation = () => {
  const { navigation } = useSelector((state) => state.project)
  const templates = useSelector((state) => state.templates)

  const currentSection = {
    id: 1
  }
  const currentPage = {
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
              <Link location={{area: 'interview', pageId: section.first}}>
                {section.title}
              </Link>
              {
                (section.id === currentSection?.id) && (
                  <ul className="list-unstyled">
                    {
                      section.pages.map((page, pageIndex) => (
                        <li
                          key={pageIndex} className={
                            classNames('ps-4', {'active': page.id === currentPage?.id})
                          }>
                          {
                            page.show ? (
                              <Link location={{area: 'interview', pageId: page.id}}>
                                {page.title}
                              </Link>
                            ) : (
                              <span className="text-muted">{page.title}</span>
                            )
                          }
                        </li>
                      )
                      )
                    }
                  </ul>
                )
              }
            </li>
          )
          )
        }
      </ul>
    </>
  )
}

export default Navigation
