import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const CatalogInfo = ({ catalog }) => {
  return (
    <div className="element-info">
      <Html html={interpolate(ngettext(
        'This catalog is used in <b>one project</b>.',
        'This catalog is used in <b>%s projects</b>.',
        catalog.projects_count), [catalog.projects_count])} />
    </div>
  )
}

CatalogInfo.propTypes = {
  catalog: PropTypes.object.isRequired
}

export default CatalogInfo
