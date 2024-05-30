import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

const PageHelp = ({ page }) => {
  return !isEmpty(page.help) && (
    <div dangerouslySetInnerHTML={{ __html: page.help }} />
  )
}

PageHelp.propTypes = {
  page: PropTypes.object.isRequired
}

export default PageHelp
