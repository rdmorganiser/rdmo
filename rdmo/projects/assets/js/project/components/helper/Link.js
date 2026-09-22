import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { navigateDashboard } from '../../actions/navigationActions'
import { buildPath } from '../../utils/location'

const Link = ({ location, children }) => {
  const dispatch = useDispatch()

  const href = buildPath(location)

  const handleClick = (event) => {
    event.preventDefault()
    dispatch(navigateDashboard(location))
  }

  return (
    <a href={href} onClick={handleClick}>
      {children}
    </a>
  )
}

Link.propTypes = {
  location: PropTypes.object.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node]),
}

export default Link
