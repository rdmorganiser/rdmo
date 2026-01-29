import React from 'react'
import { useSelector } from 'react-redux'

import Dashboard from './areas/Dashboard'
import Interview from './areas/Interview'
import Documents from './areas/Documents'
import Information from './areas/Information'
import Memberships from './areas/Memberships'
import Snapshots from './areas/Snapshots'
import Plugins from './areas/Plugins'

import View from './helper/View'

const Main = () => {
  const { area, snapshotId } = useSelector((state) => state.config)
  const { project, currentView } = useSelector((state) => state.project)

  const renderArea = () => {
    switch (area) {
      case 'dashboard':
        return <Dashboard />
      case 'interview':
        return <Interview />
      case 'documents':
        return currentView ? <View /> : <Documents />
      case 'snapshots':
        return currentView ? <View /> : (snapshotId ? <Documents /> : <Snapshots />)
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

  return area && project && (
    <div className="py-4 ps-4 pe-5">
      <div className="container gx-0">
        {renderArea()}
      </div>
    </div>
  )
}

export default Main
