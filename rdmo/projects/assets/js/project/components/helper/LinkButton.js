import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import { navigateDashboard } from '../../actions/navigationActions'

const LinkButton = ({ location, children }) => {
  const dispatch = useDispatch()

  const handleClick = (event) => {
    event.preventDefault()
    dispatch(navigateDashboard(location))
  }

  return (
    <button className="link" onClick={handleClick}>
      {children}
    </button>
  )
}

LinkButton.propTypes = {
  location: PropTypes.object.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node]),
}

export default LinkButton
