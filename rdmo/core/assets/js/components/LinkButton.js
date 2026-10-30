import React from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const LinkButton = ({ title, className, disabled = false, stopPropagation = true, onClick, children }) => {
  const handleClick = (event) => {
    event.preventDefault()
    if (stopPropagation) event.stopPropagation()
    if (!disabled) onClick()
  }

  return (
    <button
      type="button"
      title={title}
      aria-label={title}
      className={classNames('link', className)}
      disabled={disabled}
      onClick={event => handleClick(event)}
    >
      {children}
    </button>
  )
}

LinkButton.propTypes = {
  title: PropTypes.string,
  className: PropTypes.string,
  disabled: PropTypes.bool,
  stopPropagation: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export default LinkButton
