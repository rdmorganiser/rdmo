import React from 'react'
import { useSelector } from 'react-redux'
import { isNil } from 'lodash'

import Errors from 'rdmo/core/assets/js/components/Errors'

import Dashboard from './areas/Dashboard'
import Documents from './areas/Documents'
import Information from './areas/Information'
import Integrations from './areas/Integrations'
import Interview from './areas/Interview'
import Memberships from './areas/Memberships'
import Snapshots from './areas/Snapshots'
import View from './helper/View'

const Main = () => {
  const { area, snapshotId, viewId, detail } = useSelector((state) => state.location)
  const { project } = useSelector((state) => state.project)
  const showView = !isNil(viewId) || ['questions', 'answers'].includes(detail)

  const renderArea = () => {
    switch (area) {
      case 'dashboard':
        return <Dashboard />
      case 'interview':
        return <Interview />
      case 'documents':
        return showView ? <View /> : <Documents />
      case 'snapshots':
        return showView ? <View /> : (snapshotId ? <Documents /> : <Snapshots />)
      case 'information':
        return <Information />
      case 'memberships':
        return <Memberships />
      case 'integrations':
        return <Integrations />
      default:
        return <h2>Page Not Found</h2>
    }
  }

  return area && project && (
    <div className="container-lg gx-0">
      <Errors />
      {renderArea()}
    </div>
  )
}

export default Main
