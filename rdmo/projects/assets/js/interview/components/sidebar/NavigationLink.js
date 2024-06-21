import React from 'react'
import PropTypes from 'prop-types'

const NavigationLink = ({ element, href, onClick }) => {

  const label = interpolate(gettext('(%s of %s)'), [element.count, element.total])

  const handleClick = (event,) => {
    event.preventDefault()
    onClick()
  }

  return (
    <a href={href} onClick={handleClick}>
      {element.title}
      {
        element.count > 0 && element.count == element.total && (
          <span>
            {' '}<i className="fa fa-check" aria-hidden="true"></i>
          </span>
        )
      }
      {
        element.count > 0 && element.count != element.total && (
          <>
            {' '}<span>{label}</span>
          </>
        )
      }
    </a>
  )
}

NavigationLink.propTypes = {
  element: PropTypes.object.isRequired,
  href: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

export default NavigationLink
