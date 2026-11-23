import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const Link = ({ href = '', title, className, disabled = false, stopPropagation = true, onClick, children }) => {
  const handleClick = (event) => {
    event.preventDefault()
    if (stopPropagation) event.stopPropagation()
    if (!disabled) onClick()
  }

  return (
    <a
      href={href}
      title={title}
      aria-label={title}
      className={classNames(className, { disabled })}
      onClick={event => handleClick(event)}
    >
      {children}
    </a>
  )
}

Link.propTypes = {
  href: PropTypes.string,
  title: PropTypes.string,
  className: PropTypes.string,
  disabled: PropTypes.bool,
  stopPropagation: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default Link
