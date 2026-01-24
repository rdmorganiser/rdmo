import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classnames from 'classnames'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { navigateDashboard } from '../actions/projectActions'

const Sidebar = () => {
  const dispatch = useDispatch()

  const { panel } = useSelector((state) => state.config)
  const { project } = useSelector((state) => state.project)

  const catalog = project?.catalogs.find(catalog => catalog.id == project.project.catalog)

  const menuItems = [
    {
      title: '',
      items: [
        { panel: 'dashboard', name: gettext('Dashboard'), icon: 'bi-grid' }
      ],
    },
    {
      title: gettext('Data management plan'),
      items: [
        { panel: 'interview', name: gettext('Interview'), icon: 'bi-clipboard-check' },
        { panel: 'documents', name: gettext('Documents'), icon: 'bi-file-text' },
        { panel: 'snapshots', name: gettext('Snapshots'), icon: 'bi-stack' },
      ],
    },
    {
      title: gettext('Settings'),
      items: [
        { panel: 'information', name: gettext('Project data'), icon: 'bi-info-square' },
        { panel: 'memberships', name: gettext('Membership'), icon: 'bi-people' },
        { panel: 'plugins', name: gettext('Plugins'), icon: 'bi-wrench' },
      ],
    },
  ]

  return project && (
    <div className="d-flex flex-column h-100 p-4">

      <div className="card w-100 mb-3">
        <div className="card-body py-2">
          <h2 className="font-large mb-2">{project.project.title}</h2>
          <p className="font-normal text-muted m-0">{catalog.title}</p>
        </div>
      </div>

      <div className="flex-grow-1">
      {
        menuItems.map((group, groupIndex) => (
          <div key={groupIndex}>
            {
              group.title && <h3 className="font-small px-3 my-3">{group.title}</h3>
            }

            <ul className="nav nav-pills nav-fill flex-column">
            {
              group.items.map((item, itemIndex) => (
                <li key={itemIndex} className="nav-item">
                  <button
                    className={classnames('nav-link', { active: panel === item.panel })}
                    onClick={() => dispatch(navigateDashboard({ panel: item.panel }))}
                  >
                    <div className="d-flex align-items-center gap-2">
                      <i className={`bi ${item.icon}`}></i>
                      {item.name}
                    </div>
                  </button>
                </li>
              ))
            }
            </ul>
          </div>
        ))
      }
      </div>

      <hr />

      <div>
        <a href={`${baseUrl}/projects/`}
          className="nav-link text-dark w-100 text-start d-flex align-items-center gap-2">
          <i className="bi bi-arrow-left"></i> {gettext('Back to projects overview')}
        </a>
      </div>
    </div>
  )
}

export default Sidebar
