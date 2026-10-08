import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { stripTags } from 'rdmo/core/assets/js/utils/html'

import Link from 'rdmo/core/assets/js/components/Link'

import { navigateDashboard } from '../../actions/navigationActions'
import { buildPath } from '../../utils/location'

const LocationLink = ({ title, location, children }) => {
  const dispatch = useDispatch()

  return (
    <Link
      title={stripTags(title)}
      href={buildPath(location)}
      onClick={() => dispatch(navigateDashboard(location))}
    >
      {children}
    </Link>
  )
}

LocationLink.propTypes = {
  title: PropTypes.string,
  location: PropTypes.object.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node]),
}

export default LocationLink
