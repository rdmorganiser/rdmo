import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const Link = ({ href, title, className, disabled = false, stopPropagation = true, onClick, children, ...props }) => {
  const handleClick = (event) => {
    // let the browser handle modified clicks, e.g. to open the link in a new tab
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return

    event.preventDefault()
    if (stopPropagation) event.stopPropagation()
    if (!disabled) onClick(event)
  }

  return (
    <a
      href={disabled ? undefined : href}
      title={title}
      aria-label={children ? undefined : title}
      aria-disabled={disabled || undefined}
      tabIndex={disabled ? -1 : undefined}
      {...props}
      className={classNames(className, { disabled })}
      onClick={handleClick}
    >
      {children}
    </a>
  )
}

Link.propTypes = {
  href: PropTypes.string.isRequired,
  title: PropTypes.string,
  className: PropTypes.string,
  disabled: PropTypes.bool,
  stopPropagation: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default Link
