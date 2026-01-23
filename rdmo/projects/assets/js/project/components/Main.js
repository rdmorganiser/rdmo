import React from 'react'
import { useSelector } from 'react-redux'

import Dashboard from './pages/Dashboard'
import Documents from './pages/Documents'
import Snapshots from './pages/Snapshots'
import Membership from './pages/Membership'
import ProjectData from './pages/ProjectData'

const Main = () => {
  const { page, pageId } = useSelector((state) => state.config)

  const renderPage = () => {
    if (page === 'snapshots' && pageId) {
      return <Documents />
    }

    switch (page) {
      case '':
        return <Dashboard />
      case 'documents':
        return <Documents />
      case 'snapshots':
        return <Snapshots />
      case 'project-information':
        return <ProjectData />
      case 'membership':
        return <Membership />
      default:
        return <h2>Page Not Found</h2>
    }
  }

  return (
    <div className="d-flex">
      <div className="flex-grow-1 pt-4">
        <div className="container">
          {renderPage()}
        </div>
      </div>
    </div>
  )
}

export default Main
