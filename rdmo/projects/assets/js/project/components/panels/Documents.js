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
      <div className="row">
        {
          views.map((view) => (
            <ViewTile
                key={view.id}
                title={view.title}
                help={view.help}
                onClick={() => dispatch(navigateDashboard({ panel: 'documents', viewId: view.id }))}
                onExport={(format) => dispatch(downloadView(null, view.id, format))}
            />
          ))
        }
      </div>

      <h2>{gettext('Additional documents')}</h2>
      <div className="row">
        <ViewTile
          title={gettext('List all questions')}
          help={gettext('Overview of all questions')}
          onClick={() => dispatch(navigateDashboard({ panel: 'documents', detail: 'questions' }))}
          onExport={(format) => {console.log(format)}}
        />
        <ViewTile
          title={gettext('List all answers')}
          help={gettext('Overview of all questions and answers')}
          onClick={() => dispatch(navigateDashboard({ panel: 'documents', detail: 'answers' }))}
          onExport={(format) => dispatch(downloadAnswers(null, format))}
        />
      </div>
    </div>
  )
}

export default Documents
