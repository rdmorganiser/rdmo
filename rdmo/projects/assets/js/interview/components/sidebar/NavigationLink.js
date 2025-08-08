import React from 'react'
import PropTypes from 'prop-types'

const NavigationLink = ({ element, href, onClick, muted = false }) => {
  // Always prepare the label so we can show "0 of N"
  const isComplete = element.total > 0 && element.count === element.total
  const showLabel = element.total > 0 && !isComplete
  const label = interpolate(gettext('(%s of %s)'), [element.count, element.total])

  const handleClick = (event) => {
    event.preventDefault()
    onClick()
  }

  // If muted (e.g., section.show === false or page.show === false)
  if (muted) {
    return (
      <span className="text-muted">
        {element.title}
        {isComplete && (
          <span aria-label={gettext('Complete')}>
            {' '}<i className="fa fa-check" aria-hidden="true"></i>
          </span>
        )}
        {showLabel && (
          <span aria-label={label}>
            {' '}<span>{label}</span>
          </span>
        )}
      </span>
    )
  }

  // Interactive link (default)
  return (
    <a href={href} onClick={handleClick}>
      {element.title}
      {isComplete && (
        <span aria-label={gettext('Complete')}>
          {' '}<i className="fa fa-check" aria-hidden="true"></i>
        </span>
      )}
      {showLabel && (
        <span aria-label={label}>
          {' '}<span>{label}</span>
        </span>
      )}
    </a>
  )
}

NavigationLink.propTypes = {
  element: PropTypes.object.isRequired,
  href: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  muted: PropTypes.bool
}

export default NavigationLink
