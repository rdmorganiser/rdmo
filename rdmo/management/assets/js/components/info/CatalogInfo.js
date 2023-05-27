import React from 'react'
import PropTypes from 'prop-types'

const CatalogInfo = ({ catalog }) => {
  return (
    <div className="element-info">
      <p dangerouslySetInnerHTML={{
        __html: interpolate(ngettext(
          'This catalog is used in <b>one project</b>.',
          'This catalog is used in <b>%s projects</b>.',
          catalog.projects_count), [catalog.projects_count])}} />
    </div>
  )
}

CatalogInfo.propTypes = {
  catalog: PropTypes.object.isRequired
}

export default CatalogInfo
