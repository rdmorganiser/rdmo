import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import * as configActions from 'rdmo/core/assets/js/actions/configActions'

import Select from 'rdmo/core/assets/js/components/forms/Select'

import { navigateDashboard, updateProjectTask } from '../../actions/projectActions'
import { Tile } from '../helper'

const Dashboard = () => {
  const dispatch = useDispatch()
  const config = useSelector(state => state.config)
  const perms = useSelector(state => state.project.project.project.permissions) ?? {}
  const issues = useSelector((state) => state.project.project.tasks) ?? []
  // const allIssues = useSelector((state) => state.project.project.tasks) ?? []
  const resolvedIssues = issues.filter((issue) => issue.resolve === true)
  console.log('resolved issues', resolvedIssues)
  // const issues = allIssues.filter((issue) => issue.resolve === true)
  // console.log('resolved issues', issues)

  console.log('all issues', issues)
  const statusOptions = [
    { value: 'open', label: gettext('Open') },
    { value: 'closed', label: gettext('Closed') },
    { value: 'in_progress', label: gettext('In progress') },
  ]

  const { showClosedTasks, showClosedRecommendations } = config

  console.log('showClosedTasks', showClosedTasks)
  console.log('showClosedRecommendations', showClosedRecommendations)
  const [selectedTaskIssue, setSelectedTaskIssue] = useState(null)

  const isClosed = (issue) => issue.status === 'closed'
  const getTaskType = (issue) => issue.task?.task_type

  const stepIssues = issues.filter((issue) =>
    getTaskType(issue) === 'step'
  ).sort((a, b) => a.task.order - b.task.order)

  const taskIssues = issues.filter((issue) =>
    getTaskType(issue) === 'task'
  )

  const visibleTaskIssues = taskIssues
    .filter((issue) => showClosedTasks || !isClosed(issue))
    .sort((a, b) => Number(isClosed(a)) - Number(isClosed(b)))

  const recommendationIssues = issues.filter((issue) =>
    getTaskType(issue) === 'recommendation'
  )

  const visibleRecommendationIssues = recommendationIssues
    .filter((issue) => showClosedRecommendations || !isClosed(issue))
    .sort((a, b) => Number(isClosed(a)) - Number(isClosed(b)))

  const guidanceIssues = issues.filter((issue) =>
    getTaskType(issue) === 'guidance'
  ).sort((a, b) => a.task.order - b.task.order)

  const toggleTaskDone = (issueId, currentStatus) => {
    console.log('toggle issue', issueId)
    dispatch(updateProjectTask(issueId, {
      status: currentStatus === 'closed' ? 'open' : 'closed'
    }))
  }

  const renderIssueTiles = (visibleIssues) => (
    <div className="row">
      {
        visibleIssues.map((issue) => {
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
                    disabled={!perms.can_change_issue}
                    onClick={
                      (e) => {
                        e.stopPropagation()
                        toggleTaskDone(issue.id, issue.status)
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
                  <div className="text-muted small mt-2 text-end">
                    <i className="bi bi-clock me-1" />
                    {issue.dates?.[0] ?? ''}
                  </div>
                </div>
              </div>
            </Tile>
          )
        })
      }
    </div>
  )

  return (
    <div>
      <h1>{gettext('Dashboard')}</h1>
      {
        perms.can_view_issue && (
          <>
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
                          label={`${gettext('Step')} ${index + 1}`}
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
                      onChange={() => dispatch(configActions.updateConfig('showClosedTasks', !showClosedTasks))}
                    />
                    <label className="form-check-label" htmlFor="showClosedTasks">
                      {gettext('Show closed tasks')}
                    </label>
                  </div>
                  {renderIssueTiles(visibleTaskIssues)}
                </>
              )
            }
            {
              recommendationIssues.length > 0 && (
                <>
                  <h2>{gettext('Recommendations')}</h2>

                  <div className="form-check form-switch mb-3">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      id="showClosedRecommendations"
                      checked={showClosedRecommendations}
                      onChange={
                        () => dispatch(configActions.updateConfig(
                          'showClosedRecommendations',
                          !showClosedRecommendations
                        ))
                      }
                    />
                    <label className="form-check-label" htmlFor="showClosedRecommendations">
                      {gettext('Show closed tasks')}
                    </label>
                  </div>
                  {renderIssueTiles(visibleRecommendationIssues)}
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
                <Modal
                  show
                  title={selectedTaskIssue.task.title}
                  onClose={() => setSelectedTaskIssue(null)}
                  size="modal-lg"
                >
                  <p>{selectedTaskIssue.id}</p>
                  <p>{selectedTaskIssue.task.text}</p>
                  {/* <p>{selectedTaskIssue.status}</p> */}
                  <Select
                    isDisabled={!perms.can_change_issue}
                    label={gettext('Status')}
                    options={statusOptions}
                    value={selectedTaskIssue.status}
                    onChange={
                      (status) => {
                        dispatch(updateProjectTask(selectedTaskIssue.id, { status }))
                        setSelectedTaskIssue({
                          ...selectedTaskIssue,
                          status,
                        })
                      }
                    }
                  />
                  <p>{`URI: ${selectedTaskIssue.task.uri}`}</p>
                  <p>{selectedTaskIssue.dates?.[0]}</p>
                  <p>{`Condition Uris: ${(selectedTaskIssue.task.condition_uris ?? []).join(', ')}`}</p>
                </Modal>
              )
            }
          </>
        )
      }
    </div>
  )
}

export default Dashboard
