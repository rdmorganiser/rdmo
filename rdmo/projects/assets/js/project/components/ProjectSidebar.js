import React from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'
import { useDispatch, useSelector } from 'react-redux'

import { setPage } from '../actions/projectActions'

import ProjectBadge from './helper/ProjectBadge'

const ProjectSidebar = ({ menuItems }) => {
  const page = useSelector((state) => state.config.page)
  const dispatch = useDispatch()

  return (
    <div className="project-sidebar p-2">
      <ProjectBadge />

      <ul className="nav nav-pills flex-column mb-auto">
        {menuItems.map((section) => (
          <div key={section.title}>
            {section.title && <h6 className="text-muted mt-3 mb-2">{section.title}</h6>}

            {section.items.map((item) => (
              <li key={item.id} className="nav-item">
                <button
                  className={classnames('nav-link w-100 text-start d-flex align-items-center gap-2', {
                    active: page === item.id
                  })}
                  onClick={() => dispatch(setPage(item.id))}
                >
                  <i className={`bi ${item.icon}`}></i>
                  {item.name}
                </button>
              </li>
            ))}
          </div>
        ))}
      </ul>

      <div className="p-3 mt-auto">
        {/* <a href="/projects" className="nav-link text-dark w-100 text-start d-flex align-items-center gap-2"> */}
        <a href="/projects" className="nav-link text-light w-100 text-start d-flex align-items-center gap-2">

          <i className="bi bi-arrow-left"></i> {gettext('Back to projects overview')}
        </a>
      </div>
    </div>
  )
}

ProjectSidebar.propTypes = {
  menuItems: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string,
      items: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.string.isRequired,
          name: PropTypes.string.isRequired,
          icon: PropTypes.string,
        })
      ).isRequired,
    })
  ).isRequired
}

export default ProjectSidebar
