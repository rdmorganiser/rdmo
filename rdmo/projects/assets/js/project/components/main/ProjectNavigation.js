import React, { useState, useEffect } from 'react'
// import Sidebar from './Sidebar'
import ReactiveSidebar from './ReactiveSidebar'
// import OffcanvasSidebar from './OffcanvasSidebar'
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
      items: [{ id: 'dashboard', name: 'Dashboard', icon: 'bi-grid' }],
    },
    {
      title: 'DATENMANAGEMENTPLAN',
      items: [
        { id: 'questionnaire', name: 'Fragebogen', icon: 'bi-clipboard-check' },
        { id: 'documents', name: 'Dokumente', icon: 'bi-file-text' },
        { id: 'intermediate-states', name: 'Zwischenstände', icon: 'bi-stack' },
      ],
    },
    {
      title: 'EINSTELLUNGEN',
      items: [
        { id: 'project-data', name: 'Projektdaten', icon: 'bi-info-square' },
        { id: 'project-team', name: 'Projektteam', icon: 'bi-people' },
        { id: 'plugins', name: 'Plugins', icon: 'bi-wrench' },
      ],
    },
  ]

  // return (
  //   <div className="d-flex" style={{ height: '100vh' }}>
  //     <div style={{ width: '250px', overflow: 'hidden' }}>
  //       <ReactiveSidebar onNavigate={handleNavigation} menuItems={menuItems} activePage={activePage} />
  //       {/* <Sidebar onNavigate={handleNavigation} menuItems={menuItems} activePage={activePage} /> */}
  //       {/* <OffcanvasSidebar onNavigate={handleNavigation} menuItems={menuItems} activePage={activePage} /> */}
  //     </div>

  //     <div className="flex-grow-1 p-4" style={{ overflowY: 'auto', height: '100vh' }}>
  //       <ProjectPage activePage={activePage} />
  //     </div>
  //   </div>
  // )

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
