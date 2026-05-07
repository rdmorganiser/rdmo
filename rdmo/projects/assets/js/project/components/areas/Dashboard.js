import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { navigateDashboard } from '../../actions/projectActions'
import { Tile } from '../helper'

const Dashboard = () => {
  const dispatch = useDispatch()
  const issues = useSelector((state) => state.project.project.tasks) ?? []

  const [selectedTaskIssue, setSelectedTaskIssue] = useState(null)
  const [showClosedTasks, setShowClosedTasks] = useState(false)

  const isClosed = (issue) => issue.status === 'closed'
  const isActive = (issue) => ['open', 'in_progress'].includes(issue.status)
  const getTaskType = (issue) => issue.task?.task_type

  const stepIssues = issues.filter((issue) =>
    getTaskType(issue) === 'step' && isActive(issue)
  )

  const taskIssues = issues.filter((issue) =>
    getTaskType(issue) === 'task'
  )

  const visibleTaskIssues = taskIssues
    .filter((issue) => showClosedTasks || !isClosed(issue))
    .sort((a, b) => Number(isClosed(a)) - Number(isClosed(b)))

  const guidanceIssues = issues.filter((issue) =>
    getTaskType(issue) === 'guidance' && isActive(issue)
  )

  const toggleTaskDone = (issueId) => {
    // local placeholder until backend POST/PATCH exists
    console.log('toggle issue', issueId)
  }

  return (
    <div>
      <h1>{gettext('Dashboard')}</h1>

      {
        stepIssues.length > 0 && (
          <>
            <h2>{gettext('Create your data management plan')}</h2>
            <div className="row mb-4">
              {
                stepIssues.map((issue, index) => (
                  <Tile
                    key={issue.id}
                    title={issue.task.title}
                    label={gettext('Step %(number)s').replace('%(number)s', index + 1)}
                    buttonLabel={issue.task.task_area_display}
                    onClick={
                      issue.task.task_area ? (
                        () => dispatch(navigateDashboard({ area: issue.task.task_area }))
                      ) : undefined
                    }
                  >
                    <p>{issue.task.text}</p>
                  </Tile>
                ))
              }
            </div>
          </>
        )
      }

      {
        taskIssues.length > 0 && (
          <>
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
                visibleTaskIssues.map((issue) => {
                  const closed = isClosed(issue)

                  return (
                    <Tile
                      key={issue.id}
                      size="normal"
                      onCardClick={() => setSelectedTaskIssue(issue)}
                    >
                      <div className="d-flex align-items-start">
                        <div className="me-3 mt-1">
                          <button
                            type="button"
                            className="btn p-0 border-0 bg-transparent"
                            onClick={
                              (e) => {
                                e.stopPropagation()
                                toggleTaskDone(issue.id)
                              }
                            }
                            aria-label={closed ? 'Mark task as not done' : 'Mark task as done'}
                          >
                            <i className={`bi ${closed ? 'bi-check-circle-fill' : 'bi-circle'}`} />
                          </button>
                        </div>

                        <div className="flex-grow-1">
                          <div className={closed ? 'fw-semibold text-muted' : 'fw-semibold'}>
                            {issue.task.title}
                          </div>

                          <div className="d-flex justify-content-between text-muted small mt-2">
                            <div>
                              <i className="bi bi-check2-square me-1" />
                              {issue.resolve ? '1 / 1' : '0 / 1'}
                            </div>

                            <div>
                              <i className="bi bi-clock me-1" />
                              {issue.dates?.[0] ?? ''}
                            </div>
                          </div>
                        </div>
                      </div>
                    </Tile>
                  )
                })
              }
            </div>
          </>
        )
      }

      {
        guidanceIssues.length > 0 && (
          <>
            <h2>{gettext('More actions')}</h2>
            <div className="row mb-4">
              {
                guidanceIssues.map((issue) => (
                  <Tile
                    key={issue.id}
                    title={issue.task.title}
                    buttonLabel={issue.task.task_area_display}
                    onClick={
                      issue.task.task_area ? (
                        () => dispatch(navigateDashboard({ area: issue.task.task_area }))
                      ) : undefined
                    }
                    size="compact"
                  >
                    <p>{issue.task.text}</p>
                  </Tile>
                ))
              }
            </div>
          </>
        )
      }

      {
        selectedTaskIssue && (
          <div className="modal d-block" tabIndex="-1">
            <div className="modal-dialog">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">{selectedTaskIssue.task.title}</h5>
                  <button
                    type="button"
                    className="btn-close"
                    onClick={() => setSelectedTaskIssue(null)}
                  />
                </div>
                <div className="modal-body">
                  <p>{selectedTaskIssue.task.text}</p>
                  <p>{selectedTaskIssue.dates?.[0]}</p>
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
