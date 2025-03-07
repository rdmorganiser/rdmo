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
          <span aria-label={gettext('Complete')}>
            {' '}<i className="fa fa-check" aria-hidden="true"></i>
          </span>
        )
      }
      {
        element.count > 0 && element.count != element.total && (
          <span aria-label={label}>
            {' '}<span>{label}</span>
          </span>
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
