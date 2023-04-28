import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Link = ({ href="", onClick, children }) => {
    const handleClick = (event) => {
        event.preventDefault()
        onClick()
    }

    return (
        <a href={href} onClick={event => handleClick(event)}>
            {children}
        </a>
    )
}

Link.propTypes = {
  href: PropTypes.string,
  onClick: PropTypes.func.isRequired
}

export default Link
