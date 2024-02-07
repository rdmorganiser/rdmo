import React from 'react'
import PropTypes from 'prop-types'

const ViewInfo = ({ view }) => {
  return (
    <div className="element-info">
      <p dangerouslySetInnerHTML={{
        __html: interpolate(ngettext(
          'This view is used in <b>one project</b>.',
          'This view is used in <b>%s projects</b>.',
          view.projects_count
        ), [view.projects_count])}} />
    </div>
  )
}

ViewInfo.propTypes = {
  view: PropTypes.object.isRequired
}

export default ViewInfo
