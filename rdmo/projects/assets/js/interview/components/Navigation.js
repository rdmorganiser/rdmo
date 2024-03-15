import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const Navigation = ({ currentPage, navigation, onJump }) => {

  const handleJump = (event, section, page) => {
    event.preventDefault()
    onJump(section, page)
  }

  return (
    <>
      <h2>{gettext('Navigation')}</h2>

      <ul className="list-unstyled interview-navigation">
        {
          navigation.map((section, sectionIndex) => (
            <li key={sectionIndex}>
              <a href="" onClick={event => handleJump(event, section)}>
                {section.title}
              </a>
              {
                section.pages && (
                  <ul className="list-unstyled">
                    {
                      section.pages.map((page, pageIndex) => (
                        <li key={pageIndex} className={classNames({'active': page.id == currentPage.id})}>
                          {
                            page.show ? (
                              <a href="" onClick={event => handleJump(event, section, page)}>
                                <span>{page.title}</span>
                                {
                                  page.count > 0 && page.count == page.total && (
                                    <span>
                                      <i className="fa fa-check" aria-hidden="true"></i>
                                    </span>
                                  )
                                }
                                {
                                  page.count > 0 && page.count != page.total && (
                                    <span dangerouslySetInnerHTML={{
                                      __html: interpolate(gettext('(%s of %s)'), [page.count, page.total])}} />
                                  )
                                }
                              </a>
                            ) : (
                              <span className="text-muted">{page.title}</span>
                            )
                          }
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

Navigation.propTypes = {
  currentPage: PropTypes.object.isRequired,
  navigation: PropTypes.array.isRequired,
  onJump: PropTypes.func.isRequired
}

export default Navigation
