import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import Html from './Html'

const Template = ({ template, id, className }) => {
  const html = useSelector((state) => state.templates?.[template])

  return <Html id={id} className={className} html={html} />
}

Template.propTypes = {
  template: PropTypes.string.isRequired,
  id: PropTypes.string,
  className: PropTypes.string
}

export default Template
