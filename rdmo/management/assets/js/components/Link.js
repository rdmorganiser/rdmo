import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Link = ({ resource, id, onClick, children }) => {
    const handleClick = (event) => {
        event.preventDefault()
        onClick({ resource, id })
    }

    return (
        <a href="" onClick={event => handleClick(event)}>
            {children}
        </a>
    )
}

Link.propTypes = {
  onClick: PropTypes.func.isRequired,
  resource: PropTypes.string,
  id: PropTypes.number,
}

export default Link
