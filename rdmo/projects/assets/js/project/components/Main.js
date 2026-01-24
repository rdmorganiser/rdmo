import React from 'react'
import { useSelector } from 'react-redux'

import Dashboard from './panels/Dashboard'
import Interview from './panels/Interview'
import Documents from './panels/Documents'
import Information from './panels/Information'
import Memberships from './panels/Memberships'
import Snapshots from './panels/Snapshots'
import Plugins from './panels/Plugins'

import View from './helper/View'

const Main = () => {
  const { panel } = useSelector((state) => state.config)
  const { project, currentView } = useSelector((state) => state.project)

  const renderPanel = () => {
    switch (panel) {
      case 'dashboard':
        return <Dashboard />
      case 'interview':
        return <Interview />
      case 'documents':
        return currentView ? <View /> : <Documents />
      case 'snapshots':
        return currentView ? <View /> : <Snapshots />
      case 'information':
        return <Information />
      case 'memberships':
        return <Memberships />
      case 'plugins':
        return <Plugins />
      default:
        return <h2>Page Not Found</h2>
    }
  }

  return panel && project && (
    <div className="py-4 ps-4 pe-5">
      <div className="container gx-0">
        {renderPanel()}
      </div>
    </div>
  )
}

export default Main
