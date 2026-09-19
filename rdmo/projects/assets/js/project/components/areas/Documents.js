import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isNil } from 'lodash'

import { downloadAnswers, downloadView, navigateDashboard } from '../../actions/projectActions'
import { paramsFromConfig } from '../../utils/documentoptions'

import DocumentOptions from '../helper/DocumentOptions'
import SnapshotsDropdown from '../helper/SnapshotsDropdown'
import ViewTile from '../helper/ViewTile'

const Documents = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const { snapshotId, viewId, detail } = useSelector((state) => state.config)
  const { views } = useSelector((state) => state.project.project) ?? {}
  const area = snapshotId ? 'snapshots' : 'documents'

  const handleSnapshotChange = (snapshot) => {
    if (isNil(snapshot)) {
      dispatch(navigateDashboard({ area: 'documents', viewId, detail }))
    } else {
      dispatch(navigateDashboard({ area: 'snapshots', snapshotId: snapshot.id, viewId, detail }))
    }
  }

  return (
    <div className="project-documents">
      <div className="d-lg-flex justify-content-between align-items-center mb-5">
        <h1 className="mb-lg-0">{gettext('Documents')}</h1>
        <SnapshotsDropdown onChange={handleSnapshotChange}/>
      </div>

      <h2>{gettext('Data management plans')}</h2>
      <div className="row mb-4">
        {
          views.map((view) => (
            <div key={view.id} className="col-lg-6">
              <ViewTile
                title={view.title}
                help={view.help}
                onClick={() => dispatch(navigateDashboard({ area, snapshotId, viewId: view.id }))}
                onExport={(format) => dispatch(downloadView(snapshotId, view.id, format))}
              />
            </div>
          ))
        }
      </div>

      <h2>{gettext('Additional documents')}</h2>
      <div className="row mb-4">
        <div className="col-lg-6">
          <ViewTile
            title={gettext('Configurable list of questions')}
            help={gettext('Overview of all questions. Optionally with answers and/or help texts.')}
            onClick={() => dispatch(navigateDashboard({ area, snapshotId, detail: 'answers' }))}
            onExport={
              (format) => {
                dispatch(downloadAnswers(snapshotId, format, paramsFromConfig(config)))
              }
            }
            additionalExportItems={
              (
                <>
                  <DocumentOptions/>
                  <hr />
                </>
              )
            }
          />
        </div>
      </div>
    </div>
  )
}

export default Documents
