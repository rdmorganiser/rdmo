import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Link = ({ resourceType, resourceId, onClick, children }) => {
    const handleClick = (event) => {
        event.preventDefault()
        onClick({ resourceType, resourceId })
    }

    return (
        <a href="" onClick={event => handleClick(event)}>
            {children}
        </a>
    )
}

Link.propTypes = {
  onClick: PropTypes.func.isRequired,
  resourceType: PropTypes.string,
  resourceId: PropTypes.number,
}

export default Link
