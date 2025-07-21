import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const PageTabsHelp = ({ templates, disabled }) => {
  return !disabled && <Html html={templates.project_interview_page_tabs_help} />
}

PageTabsHelp.propTypes = {
  templates: PropTypes.object.isRequired,
  disabled: PropTypes.bool.isRequired
}

export default PageTabsHelp
