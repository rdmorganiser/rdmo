import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import Html from 'rdmo/core/assets/js/components/Html'

const Navigation = ({ currentPage, navigation, help, fetchPage }) => {

  const handleClick = (event, pageId) => {
    event.preventDefault()
    fetchPage(pageId)
  }

  return (
    <>
      <h2>{gettext('Navigation')}</h2>
      <Html html={help} />

      <ul className="list-unstyled interview-navigation">
        {
          navigation.map((section, sectionIndex) => (
            <li key={sectionIndex}>
              <a href={`/projects/12/interview/${section.first}/`} onClick={event => handleClick(event, section.first)}>
                {section.title}
              </a>
              {
                section.pages && (
                  <ul className="list-unstyled">
                    {
                      section.pages.map((page, pageIndex) => {
                        const label = interpolate(gettext('(%s of %s)'), [page.count, page.total])

                        return (
                          <li key={pageIndex} className={classNames({'active': currentPage ? page.id == currentPage.id : false})}>
                            {
                              page.show ? (
                                <a href={`/projects/12/interview/${page.id}/`} onClick={event => handleClick(event, page.id)}>
                                  <span>{page.title}</span>
                                  {
                                    page.count > 0 && page.count == page.total && (
                                      <span>
                                        {' '}<i className="fa fa-check" aria-hidden="true"></i>
                                      </span>
                                    )
                                  }
                                  {
                                    page.count > 0 && page.count != page.total && (
                                      <>
                                        {' '}<span>{label}</span>
                                      </>
                                    )
                                  }
                                </a>
                              ) : (
                                <span className="text-muted">{page.title}</span>
                              )
                            }
                          </li>
                        )
                      })
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

Navigation.propTypes = {
  currentPage: PropTypes.object,
  navigation: PropTypes.array.isRequired,
  help: PropTypes.string.isRequired,
  fetchPage: PropTypes.func.isRequired
}

export default Navigation
