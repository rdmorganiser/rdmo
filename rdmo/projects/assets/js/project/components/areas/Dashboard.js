import React from 'react'
import { useDispatch } from 'react-redux'

import { navigateDashboard } from '../../actions/projectActions'
import { Tile } from '../helper'

const Dashboard = () => {
  const dispatch = useDispatch()
  const tasks = [
    {
      title: 'Recommendation: Consider reuse scenarios',
      progress: '0 / 2',
      date: '14 August 2024',
      isDone: false,
    },
    {
      title: 'Consider Open Access Policy',
      progress: '1 / 3',
      date: '15 May 2024',
      isDone: false,
    },
    {
      title: 'Consider Open Access Policy',
      progress: '3 / 3',
      date: '15 May 2024',
      isDone: true,
    },
  ]

  return (
    <div>
      <h1>{gettext('Dashboard')}</h1>

      <h2>{gettext('Create your data management plan')}</h2>
      <div className="row mb-4">
        <Tile
          title={gettext('Answer questions')}
          label={gettext('Step 1')}
          buttonLabel={gettext('Questionnaire')}
          onClick={() => dispatch(navigateDashboard({ area: 'interview'}))}
        >
          <p>{gettext('Fill out the selected questionnaire as completely as possible.')}</p>
        </Tile>
        <Tile
          title={gettext('Export data management plan')}
          label={gettext('Step 2')}
          buttonLabel={gettext('Documents')}
          onClick={() => dispatch(navigateDashboard({ area: 'documents'}))}
        >
          <p>{gettext('Export your data management plan in various formats.')}</p>
        </Tile>
      </div>

      <h2>{gettext('Tasks')}</h2>
      <div className="row">
        {
          tasks.map((task, index) => (
            <Tile key={index} size="normal">
              <div className="d-flex align-items-start">
                <div className="me-3 mt-1">
                  {
                    task.isDone ? (
                      <i className="bi bi-check-circle-fill" />
                    ) : (
                      <i className="bi bi-circle" />
                    )
                  }
                </div>

                <div className="flex-grow-1">
                  <div className={task.isDone ? 'fw-semibold text-muted' : 'fw-semibold'}>
                    {task.title}
                  </div>

                  <div className="d-flex justify-content-between text-muted small mt-2">
                    <div>
                      <i className="bi bi-check2-square me-1" />
                      {task.progress}
                    </div>

                    <div>
                      <i className="bi bi-clock me-1" />
                      {task.date}
                    </div>
                  </div>
                </div>
              </div>
            </Tile>
          ))
        }
      </div>

      <h2>{gettext('More actions')}</h2>
      <div className="row mb-4">
        <Tile
          title={gettext('Invite team members')}
          buttonLabel={gettext('Project team')}
          onClick={() => dispatch(navigateDashboard({ area: 'memberships'}))}
          size="compact"
        >
          <p>{gettext('Invite additional people to collaborate on creating your data management plan.')}</p>
        </Tile>
        <Tile
          title={gettext('Create snapshot')}
          buttonLabel={gettext('Snapshots')}
          onClick={() => dispatch(navigateDashboard({ area: 'snapshots'}))}
          size="compact"
        >
          <p>{gettext('Save a snapshot to view or restore later.')}</p>
        </Tile>
      </div>
    </div>
  )
}

export default Dashboard
