import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isNil } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'

import { downloadAnswers, downloadView, navigateDashboard } from '../../actions/projectActions'
import { paramsFromConfig } from '../../utils/documentoptions'

import DocumentOptionsDropdown from './DocumentOptionsDropdown'
import ExportsDropdown from './ExportsDropdown'
import SnapshotsDropdown from './SnapshotsDropdown'

const View = () => {
  const dispatch = useDispatch()

  const { snapshotId, viewId, detail } = useSelector((state) => state.config)
  const config = useSelector((state) => state.config)
  const { currentView } = useSelector((state) => state.project)

  const reloadView = () => {
    const area = snapshotId == null ? 'documents' : 'snapshots'
    dispatch(navigateDashboard({area, snapshotId, viewId, detail}))
  }

  const handleSnapshotChange = (snapshot) => {
    if (isNil(snapshot)) {
      dispatch(navigateDashboard({ area: 'documents', snapshotId: null, viewId, detail }))
    } else {
      dispatch(navigateDashboard({ area: 'snapshots', snapshotId: snapshot.id, viewId, detail }))
    }
  }

  const handleExport = (format) => {
    if (detail == 'questions') {
      dispatch(downloadAnswers(snapshotId, format, {...paramsFromConfig(config), 'hide_answers': 'true'}))
    } else if (detail == 'answers') {
      dispatch(downloadAnswers(snapshotId, format, {...paramsFromConfig(config), 'hide_answers': 'false'}))
    } else if (!isNil(viewId)) {
      dispatch(downloadView(snapshotId, viewId, format))
    }
  }

  const handleBack = () => {
    if (isNil(snapshotId)) {
      dispatch(navigateDashboard({ area: 'documents' }))
    } else {
      dispatch(navigateDashboard({ area: 'snapshots', snapshotId }))
    }
  }

  return currentView && (
    <div className="project-view">
      <div className="float-end d-flex gap-3">
        <button className="link" onClick={handleBack}>
          <i className="bi bi-arrow-left"></i> {gettext('Back')}
        </button>
        {
          ['answers', 'questions'].includes(detail) && (
            <DocumentOptionsDropdown onChanged={reloadView}/>
          )
        }
        <SnapshotsDropdown onChange={handleSnapshotChange}/>
        <ExportsDropdown onExport={handleExport} />
      </div>
      <Html html={currentView.html} />
    </div>
  )
}

export default View
