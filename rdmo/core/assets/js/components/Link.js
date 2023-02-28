import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Link = ({ onClick, children }) => {
    const handleClick = (event) => {
        event.preventDefault()
        onClick()
    }

    return (
        <a href="" onClick={event => handleClick(event)}>
            {children}
        </a>
    )
}

Link.propTypes = {
  onClick: PropTypes.func.isRequired
}

export default Link
