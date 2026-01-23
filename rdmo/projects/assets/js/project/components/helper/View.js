import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isNil } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

import { downloadAnswers, downloadView, navigateDashboard } from '../../actions/projectActions'

import SnapshotsDropdown from './SnapshotsDropdown'
import ExportsDropdown from './ExportsDropdown'

const View = () => {
  const dispatch = useDispatch()

  const { snapshotId, viewId, detail } = useSelector((state) => state.config)
  const { currentView } = useSelector((state) => state.project)

  const handleSnapshotChange = (snapshot) => {
    if (isNil(snapshot)) {
      dispatch(navigateDashboard({ panel: 'documents', snapshotId: null, viewId, detail }))
    } else {
      dispatch(navigateDashboard({ panel: 'snapshots', snapshotId: snapshot.id, viewId, detail }))
    }
  }

  const handleExport = (format) => {
    if (detail == 'answers') {
      dispatch(downloadAnswers(snapshotId, format))
    } else if (!isNil(viewId)) {
      dispatch(downloadView(snapshotId, viewId, format))
    }
  }

  return currentView && (
    <div className="project-view">
      <div className="float-end d-flex gap-3">
        <SnapshotsDropdown onChange={handleSnapshotChange}/>
        <ExportsDropdown onExport={handleExport} />
      </div>
      <Html html={currentView.html} />
    </div>
  )
}

export default View
