import React from 'react'
import PropTypes from 'prop-types'

const Template = ({ template }) => {

  return (
    <div dangerouslySetInnerHTML={{ __html: template }} />
  )
}

Template.propTypes = {
  template: PropTypes.string.isRequired
}

export default Template
