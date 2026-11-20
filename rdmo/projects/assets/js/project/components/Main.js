import React from 'react'
import { useSelector } from 'react-redux'
import { isNil } from 'lodash'

import Errors from 'rdmo/core/assets/js/components/Errors'

import Dashboard from './areas/Dashboard'
import Documents from './areas/Documents'
import Document from './areas/documents/Document'
import Information from './areas/Information'
import Integrations from './areas/Integrations'
import Interview from './areas/Interview'
import Memberships from './areas/Memberships'
import Snapshots from './areas/Snapshots'

const Main = () => {
  const { area, snapshotId, viewId, detail } = useSelector((state) => state.location)
  const { project } = useSelector((state) => state.project)
  const showDocument = !isNil(viewId) || ['questions', 'answers'].includes(detail)

  const renderArea = () => {
    switch (area) {
      case 'dashboard':
        return <Dashboard />
      case 'interview':
        return <Interview />
      case 'documents':
        return showDocument ? <Document /> : <Documents />
      case 'snapshots':
        return showDocument ? <Document /> : (snapshotId ? <Documents /> : <Snapshots />)
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
