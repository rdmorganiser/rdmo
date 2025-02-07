import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import Html from 'rdmo/core/assets/js/components/Html'

import NavigationLink from './NavigationLink'

const Navigation = ({ overview, currentPage, navigation, help, fetchPage }) => {
  return (
    <>
      <h2>{gettext('Navigation')}</h2>
      <Html html={help} />

      <ul className="list-unstyled interview-navigation">
        {
          navigation.map((section, sectionIndex) => (
              <li key={sectionIndex}>
                <NavigationLink
                  element={section}
                  href={`/projects/${overview.id}/interview/${section.first}/`}
                  onClick={() => fetchPage(section.first)}
                />
                {
                  section.pages && (
                    <ul className="list-unstyled">
                      {
                        section.pages.map((page, pageIndex) => (
                            <li key={pageIndex} className={classNames({
                              'active': currentPage ? page.id == currentPage.id : false})
                            }>
                              {
                                page.show ? (
                                  <NavigationLink
                                    element={page}
                                    href={`/projects/${overview.id}/interview/${page.id}/`}
                                    onClick={() => fetchPage(page.id)}
                                  />
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

Navigation.propTypes = {
  overview: PropTypes.object.isRequired,
  currentPage: PropTypes.object,
  navigation: PropTypes.array.isRequired,
  help: PropTypes.string.isRequired,
  fetchPage: PropTypes.func.isRequired
}

export default Navigation
