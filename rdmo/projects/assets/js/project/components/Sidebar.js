import React from 'react'
import classnames from 'classnames'
import { useDispatch, useSelector } from 'react-redux'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { navigateDashboard } from '../actions/projectActions'

import ProjectBadge from './helper/ProjectBadge'

const Sidebar = () => {
  const menuItems = [
    {
      title: '',
      items: [{ id: '', name: gettext('Dashboard'), icon: 'bi-grid' }],
    },
    {
      title: gettext('DATA MANAGEMENT PLAN'),
      items: [
        { id: 'interview', name: gettext('Interview'), icon: 'bi-clipboard-check' },
        { id: 'documents', name: gettext('Documents'), icon: 'bi-file-text' },
        { id: 'snapshots', name: gettext('Snapshots'), icon: 'bi-stack' },
      ],
    },
    {
      title: gettext('PROJECT MANAGEMENT'),
      items: [
        { id: 'project-information', name: gettext('Project data'), icon: 'bi-info-square' },
        { id: 'membership', name: gettext('Membership'), icon: 'bi-people' },
        { id: 'plugins', name: gettext('Plugins'), icon: 'bi-wrench' },
      ],
    },
  ]

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
                  onClick={() => dispatch(navigateDashboard({ page: item.id }))}
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
        <a href={`${baseUrl}/projects/`}
          className="nav-link text-dark w-100 text-start d-flex align-items-center gap-2">
          <i className="bi bi-arrow-left"></i> {gettext('Back to projects overview')}
        </a>
      </div>
    </div>
  )
}

export default Sidebar
