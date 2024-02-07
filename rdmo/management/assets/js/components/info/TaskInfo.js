import React from 'react'
import PropTypes from 'prop-types'

const TaskInfo = ({ task }) => {
  return (
    <div className="element-info">
      <p dangerouslySetInnerHTML={{
        __html: interpolate(ngettext(
          'This task is used in <b>one project</b>.',
          'This task is used in <b>%s projects</b>.',
          task.projects_count
        ), [task.projects_count])}} />
    </div>
  )
}

TaskInfo.propTypes = {
  task: PropTypes.object.isRequired
}

export default TaskInfo
