import React from 'react'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

const TaskInfo = ({ task }) => {
  return (
    <div className="mb-2">
      <Html html={interpolate(ngettext(
        'This task is used in <b>one project</b>.',
        'This task is used in <b>%s projects</b>.',
        task.projects_count
      ), [task.projects_count])} />
    </div>
  )
}

TaskInfo.propTypes = {
  task: PropTypes.object.isRequired
}

export default TaskInfo
