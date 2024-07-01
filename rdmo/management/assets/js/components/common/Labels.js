import React from 'react'
import PropTypes from 'prop-types'

const Label = ({ text, type, onClick, show = true, className = '' }) => {
  const labelClass = `label label-${type} ${className}`
  return show && (
    <span className={labelClass} onClick={onClick}>
      {text}
    </span>
  )
}

Label.propTypes = {
  text: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  onClick: PropTypes.func,
  show: PropTypes.bool,
  className: PropTypes.string,
}

export default Label
