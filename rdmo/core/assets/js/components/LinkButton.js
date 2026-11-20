import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const LinkButton = ({ className, disabled = false, stopPropagation = true, onClick, children, ...props }) => {
  const handleClick = (event) => {
    if (stopPropagation) event.stopPropagation()
    onClick(event)
  }

  return (
    <button
      aria-label={children ? undefined : props.title}
      {...props}
      type="button"
      className={classNames('link', className)}
      disabled={disabled}
      onClick={handleClick}
    >
      {children}
    </button>
  )
}

LinkButton.propTypes = {
  className: PropTypes.string,
  disabled: PropTypes.bool,
  stopPropagation: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  title: PropTypes.string,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default LinkButton
