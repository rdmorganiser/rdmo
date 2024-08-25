import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

const Html = ({ html }) => {
  return !isEmpty(html) && (
    <div dangerouslySetInnerHTML={{ __html: html }} />
  )
}

Html.defaultProps = {
  className: ''
}

Html.propTypes = {
  className: PropTypes.string,
  html: PropTypes.string
}

export default Html
