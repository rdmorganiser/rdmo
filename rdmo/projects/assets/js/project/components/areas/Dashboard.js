import React, { useState } from 'react'
import { useDispatch } from 'react-redux'

import { navigateDashboard } from '../../actions/projectActions'
import { Tile } from '../helper'

const Dashboard = () => {
  const dispatch = useDispatch()

  const [selectedTask, setSelectedTask] = useState(null)
  const [showClosedTasks, setShowClosedTasks] = useState(false)

  const [tasks, setTasks] = useState([
    {
      id: 1,
      title: 'Recommendation: Consider reuse scenarios',
      progress: '0 / 2',
      date: '14 August 2024',
      isDone: false,
    },
    {
      id: 2,
      title: 'Consider Open Access Policy',
      progress: '1 / 3',
      date: '15 May 2024',
      isDone: false,
    },
    {
      id: 3,
      title: 'Consider Open Access Policy',
      progress: '3 / 3',
      date: '15 May 2024',
      isDone: true,
    },
  ])

  const visibleTasks = tasks
    .filter((task) => showClosedTasks || !task.isDone)
    .sort((a, b) => Number(a.isDone) - Number(b.isDone))

  const toggleTaskDone = (taskId) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? { ...task, isDone: !task.isDone } : task
      )
    )
  }

  return (
    <div>
      <h1>{gettext('Dashboard')}</h1>

      <h2>{gettext('Create your data management plan')}</h2>
      <div className="row mb-4">
        <Tile
          title={gettext('Answer questions')}
          label={gettext('Step 1')}
          buttonLabel={gettext('Interview')}
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

      {/*       <h2>{gettext('Tasks')}</h2>
      <div className="row">
        {
          tasks.map((task) => (
            <Tile key={task.id} size="normal">
              <div className="d-flex align-items-start">
                <div className="me-3 mt-1">
                  <button
                    type="button"
                    className="btn p-0 border-0 bg-transparent"
                    onClick={() => toggleTaskDone(task.id)}
                    aria-label={task.isDone ? 'Mark task as not done' : 'Mark task as done'}
                  >
                    <i className={`bi ${task.isDone ? 'bi-check-circle-fill' : 'bi-circle'}`} />
                  </button>
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
      </div> */}
      <h2>{gettext('Tasks')}</h2>

      <div className="form-check form-switch mb-3">
        <input
          className="form-check-input"
          type="checkbox"
          id="showClosedTasks"
          checked={showClosedTasks}
          onChange={() => setShowClosedTasks((prev) => !prev)}
        />
        <label className="form-check-label" htmlFor="showClosedTasks">
          {gettext('Show closed tasks')}
        </label>
      </div>

      <div className="row">
        {
          visibleTasks.map((task) => (
            <Tile
              key={task.id}
              size="normal"
              onCardClick={() => setSelectedTask(task)}
            >
              <div className="d-flex align-items-start">
                <div className="me-3 mt-1">
                  <button
                    type="button"
                    className="btn p-0 border-0 bg-transparent"
                    onClick={
                      (e) => {
                        e.stopPropagation()
                        toggleTaskDone(task.id)
                      }
                    }
                    aria-label={task.isDone ? 'Mark task as not done' : 'Mark task as done'}
                  >
                    <i className={`bi ${task.isDone ? 'bi-check-circle-fill' : 'bi-circle'}`} />
                  </button>
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
      {
        selectedTask && (
          <div className="modal d-block" tabIndex="-1">
            <div className="modal-dialog">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">{selectedTask.title}</h5>
                  <button
                    type="button"
                    className="btn-close"
                    onClick={() => setSelectedTask(null)}
                  />
                </div>
                <div className="modal-body">
                  <p>{gettext('Task popup placeholder')}</p>
                  <p>{selectedTask.date}</p>
                </div>
              </div>
            </div>
          </div>
        )
      }
    </div>
  )
}

export default Dashboard
