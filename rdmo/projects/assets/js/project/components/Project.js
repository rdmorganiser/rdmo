import React from 'react'
import ProjectSidebar from './ProjectSidebar'
import ProjectPage from './ProjectPage'

const Project = () => {
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

  return (
    <div className="d-flex">
      <ProjectSidebar menuItems={menuItems} />
      <div className="flex-grow-1 pt-4">
        <div className="container">
          <ProjectPage />
        </div>
      </div>
    </div>
  )
}

export default Project
