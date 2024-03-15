import React from 'react'
import PropTypes from 'prop-types'

const Breadcrump = ({ project, page, onJump }) => {
  return (
    <ul className="interview-breadcrumb breadcrumb">
      <li>
        <a href="">{gettext('My Projects')}</a>
      </li>
      <li>
        <a href="">
          {project.title}
        </a>
      </li>
      <li>
        <a href="" onClick={() => onJump(page.section.id)}>
          {page.section.title}
        </a>
      </li>
    </ul>
  )
}

Breadcrump.propTypes = {
  project: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  onJump: PropTypes.func.isRequired
}

export default Breadcrump
