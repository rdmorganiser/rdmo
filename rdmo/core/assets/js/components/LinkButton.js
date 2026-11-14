import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const LinkButton = ({ className, disabled = false, stopPropagation = true, onClick, children, ...props }) => {
  const handleClick = (event) => {
    event.preventDefault()
    if (stopPropagation) event.stopPropagation()
    if (!disabled) onClick()
  }

  return (
    <button
      {...props}
      type="button"
      className={classNames('link', className)}
      disabled={disabled}
      onClick={event => handleClick(event)}
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
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default LinkButton
