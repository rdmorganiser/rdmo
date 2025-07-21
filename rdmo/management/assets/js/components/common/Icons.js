import React from 'react'
import PropTypes from 'prop-types'

const ReadOnlyIcon = ({ title, show }) => {
  return show && (
    <i className="element-button fa fa-ban" title={title} aria-hidden="true"></i>
  )
}

ReadOnlyIcon.propTypes = {
  title: PropTypes.string.isRequired,
  show: PropTypes.bool
}

export { ReadOnlyIcon }
