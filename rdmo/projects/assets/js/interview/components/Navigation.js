import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const Navigation = ({ page, navigation, onClick }) => {

  const handleClick = (event, pageId) => {
    event.preventDefault()
    onClick(pageId)
  }

  return (
    <>
      <h2>{gettext('Navigation')}</h2>

      <ul className="list-unstyled interview-navigation">
        {
          navigation.map((s, sIndex) => (
            <li key={sIndex}>
              <a href={`/projects/12/interview/${s.first}/`} onClick={event => handleClick(event, s.first)}>
                {s.title}
              </a>
              {
                s.pages && (
                  <ul className="list-unstyled">
                    {
                      s.pages.map((p, pIndex) => (
                        <li key={pIndex} className={classNames({'active': p.id == page.id})}>
                          {
                            p.show ? (
                              <a href={`/projects/12/interview/${page.id}/`} onClick={event => handleClick(event, p.id)}>
                                <span>{p.title}</span>
                                {
                                  p.count > 0 && p.count == p.total && (
                                    <span>
                                      <i className="fa fa-check" aria-hidden="true"></i>
                                    </span>
                                  )
                                }
                                {
                                  p.count > 0 && p.count != p.total && (
                                    <span dangerouslySetInnerHTML={{
                                      __html: interpolate(gettext('(%s of %s)'), [p.count, p.total])}} />
                                  )
                                }
                              </a>
                            ) : (
                              <span className="text-muted">{p.title}</span>
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
  page: PropTypes.object.isRequired,
  navigation: PropTypes.array.isRequired,
  onClick: PropTypes.func.isRequired
}

export default Navigation
