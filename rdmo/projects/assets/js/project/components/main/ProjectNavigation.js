import React, { useState, useEffect } from 'react'
import ReactiveSidebar from './ReactiveSidebar'
import ProjectPage from './ProjectPage'

const ProjectNavigation = () => {
  const getActivePageFromHash = () => (window.location.hash ? window.location.hash.substring(1) : 'dashboard')

  const [activePage, setActivePage] = useState(getActivePageFromHash())

  useEffect(() => {
    const handleHashChange = () => {
      setActivePage(getActivePageFromHash())
    }

    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  const handleNavigation = (id) => {
    window.location.hash = id ? `#${id}` : ''
    setActivePage(id)
  }

  const menuItems = [
    {
      title: '',
      items: [{ id: 'dashboard', name: gettext('Dashboard'), icon: 'bi-grid' }],
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
    <div className="d-flex vh-100">
      {/* Sidebar */}
      <div className="d-flex flex-column" style={{ width: '250px', height: '100vh' }}>
        <ReactiveSidebar onNavigate={handleNavigation} menuItems={menuItems} activePage={activePage} />
      </div>

      {/* Content Area */}
      <div className="flex-grow-1 overflow-auto bg-light-grey p-4">
        <ProjectPage activePage={activePage} />
      </div>
    </div>
  )
}

export default ProjectNavigation
