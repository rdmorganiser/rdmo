import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const PageHelp = ({ page }) => {
  return <div className="interview-page-help" >
    <Html html={page.help} />
  </div>
}

PageHelp.propTypes = {
  page: PropTypes.object.isRequired
}

export default PageHelp
