import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { downloadView, downloadAnswers, navigateDashboard } from '../../actions/projectActions'

import ViewTile from '../helper/ViewTile'

const Documents = () => {
  const dispatch = useDispatch()

  const { views } = useSelector((state) => state.project.project) ?? {}

  return (
    <div className="project-documents">
      <div className="d-flex justify-content-between align-items-center mb-5">
        <h1 className="mb-0">{gettext('Documents')}</h1>
      </div>

      <h2>{gettext('Data management plans')}</h2>
      <div className="row mb-4">
        {
          views.map((view) => (
            <div key={view.id} className="col-lg-6">
              <ViewTile
                  title={view.title}
                  help={view.help}
                  onClick={() => dispatch(navigateDashboard({ panel: 'documents', viewId: view.id }))}
                  onExport={(format) => dispatch(downloadView(null, view.id, format))}
              />
            </div>
          ))
        }
      </div>

      <h2>{gettext('Additional documents')}</h2>
      <div className="row mb-4">
        <div className="col-lg-6">
          <ViewTile
            title={gettext('List all questions')}
            help={gettext('Overview of all questions')}
            onClick={() => dispatch(navigateDashboard({ panel: 'documents', detail: 'questions' }))}
            onExport={(format) => {console.log(format)}}
          />
        </div>
        <div className="col-lg-6">
          <ViewTile
            title={gettext('List all answers')}
            help={gettext('Overview of all questions and answers')}
            onClick={() => dispatch(navigateDashboard({ panel: 'documents', detail: 'answers' }))}
            onExport={(format) => dispatch(downloadAnswers(null, format))}
          />
        </div>
      </div>
    </div>
  )
}

export default Documents
