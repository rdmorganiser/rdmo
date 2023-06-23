import React from 'react'
import PropTypes from 'prop-types'

const Link = ({ href='', title, className, onClick, children }) => {
    const handleClick = (event) => {
        event.preventDefault()
        onClick()
    }

    return (
        <a href={href} title={title} className={className} onClick={event => handleClick(event)}>
            {children}
        </a>
    )
}

Link.propTypes = {
  href: PropTypes.string,
  title: PropTypes.string,
  className: PropTypes.string,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default Link
