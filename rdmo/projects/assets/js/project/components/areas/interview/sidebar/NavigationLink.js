import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

import LocationLink from '../../../helper/LocationLink'

const NavigationLink = ({ element }) => {
  const label = interpolate(gettext('(%s of %s)'), [element.count, element.total])
  const location = {area: 'interview', pageId: element?.first || element.id}

  return (
    <LocationLink title={element.title} location={location}>
      <Html html={element.title} />
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
    </LocationLink>
  )
}

NavigationLink.propTypes = {
  element: PropTypes.object.isRequired,
}

export default NavigationLink
