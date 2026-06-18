import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import { useFormattedDateTime } from 'rdmo/core/assets/js/hooks'
import { language } from 'rdmo/core/assets/js/utils'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import Select from 'rdmo/core/assets/js/components/forms/Select'

import { navigateDashboard, updateProjectTask } from '../../actions/projectActions'
import { projectId } from '../../utils/meta'
import { Tile } from '../helper'

import ShowClosedIssues from './dashboard/ShowClosedIssues'

const Dashboard = () => {
  const dispatch = useDispatch()
  const config = useSelector(state => state.config)
  const perms = useSelector(state => state.project.project.project.permissions) ?? {}

  const allIssues = useSelector((state) => state.project.project.tasks) ?? []
  /* Show only issues that resolve */
  const issues = allIssues.filter((issue) => issue.resolve === true)

  // Mock dates for testing
  // issues.forEach((issue) => {
  //   issue.dates = [
  //     ['2017-04-03', '2017-12-31'],
  //     ['2017-04-03'],
  //     ['2017-04-04'],
  //   ]
  // })

  const statusOptions = [
    { value: 'open', label: gettext('Open') },
    { value: 'closed', label: gettext('Closed') },
    { value: 'in_progress', label: gettext('In progress') },
  ]

  const { showClosedTasks, showClosedRecommendations } = config

  const [selectedTaskIssue, setSelectedTaskIssue] = useState(null)

  const isClosed = (issue) => issue.status === 'closed'
  const getTaskType = (issue) => issue.task?.task_type

  const stepIssues = issues.filter((issue) =>
    getTaskType(issue) === 'step'
  ).sort((a, b) => a.task.order - b.task.order)

  const activeStepIssue = stepIssues.find((issue) => !isClosed(issue))

  const visibleTaskIssues = issues
    .filter((issue) => getTaskType(issue) === 'task' && (showClosedTasks || !isClosed(issue)))
    .sort((a, b) => Number(isClosed(a)) - Number(isClosed(b)))

  const visibleRecommendationIssues = issues
    .filter((issue) => getTaskType(issue) === 'recommendation' && (showClosedRecommendations || !isClosed(issue)))
    .sort((a, b) => Number(isClosed(a)) - Number(isClosed(b)))

  const guidanceIssues = issues.filter((issue) =>
    getTaskType(issue) === 'guidance'
  ).sort((a, b) => a.task.order - b.task.order)

  const toggleTaskDone = (issueId, currentStatus) => {
    dispatch(updateProjectTask(issueId, {
      status: currentStatus === 'closed' ? 'open' : 'closed'
    }))
  }

  const renderDate = (date) => (
    date.map((dateValue) => useFormattedDateTime(dateValue, language, 'dateOnly')).join(' - ')
  )

  const renderVisibleIssues = (visibleIssues) => (
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
                  {
                    issue.dates?.length > 0 && (
                      <div className="text-muted small mt-2 text-end">
                        <i className="bi bi-clock me-1" />
                        {renderDate(issue.dates[0])}
                      </div>
                    )
                  }
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
                      stepIssues.map((issue, index) => {
                        const isActiveStep = activeStepIssue?.id === issue.id
                        return (
                          <Tile
                            key={issue.id}
                            title={issue.task.title}
                            label={`${gettext('Step')} ${index + 1}`}
                            buttonLabel={issue.task?.task_area_display}
                            buttonClassName={isActiveStep ? 'btn-primary' : 'btn-outline-primary'}
                            buttonIconClassName="bi bi-arrow-right"
                            onClick={
                              issue.task.task_area ? (
                                () => {
                                  dispatch(navigateDashboard({ area: issue.task.task_area }))
                                  if (isActiveStep) {
                                    dispatch(updateProjectTask(issue.id, { status: 'closed'}))
                                  }
                                }
                              ) : undefined
                            }
                          >
                            <p>{issue.task.text}</p>
                          </Tile>
                        )
                      })
                    }
                  </div>
                </>
              )
            }
            {
              visibleTaskIssues.length > 0 && (
                <>
                  <h2>{gettext('Tasks')}</h2>
                  <ShowClosedIssues
                    id="showClosedTasks"
                    label={gettext('Show closed tasks')}
                    checked={showClosedTasks}
                    onChange={() => dispatch(configActions.updateConfig('showClosedTasks', !showClosedTasks))}
                  />
                  {renderVisibleIssues(visibleTaskIssues)}
                </>
              )
            }
            {
              visibleRecommendationIssues.length > 0 && (
                <>
                  <h2>{gettext('Recommendations')}</h2>
                  <ShowClosedIssues
                    id="showClosedRecommendations"
                    label={gettext('Show closed recommendations')}
                    checked={showClosedRecommendations}
                    onChange={
                      () => dispatch(configActions.updateConfig(
                        'showClosedRecommendations',
                        !showClosedRecommendations
                      ))
                    }
                  />
                  {renderVisibleIssues(visibleRecommendationIssues)}
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
                          buttonIconClassName="bi bi-arrow-right"
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
                  {/* <p>{selectedTaskIssue.id}</p> */}
                  <p>{selectedTaskIssue.task.text}</p>
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
                  <div className="row mt-3">
                    <div className={selectedTaskIssue.dates?.length > 0 ? 'col-md-8' : 'col-md-12'}>
                      {/* questions */}
                      {
                        selectedTaskIssue.questions?.length > 0 && (
                          <>
                            <div className="fw-bold mb-2">{gettext('Why is this task shown?')}</div>
                            <p>{gettext('This task is shown based on your answers:')}</p>
                            {
                              selectedTaskIssue.questions.map((question) => (
                                <div key={question.id} className="mb-3">
                                  {
                                    question.pages?.map((page) => {
                                      const url = `${baseUrl}/projects/${projectId}/interview/${page.id}/`

                                      return (
                                        <div key={page.id}>
                                          <p>{gettext('QUESTION:')} <a href={url}>{question.text}</a></p>
                                        </div>
                                      )
                                    })
                                  }
                                  {/* conditions */}
                                  {
                                    selectedTaskIssue.task.conditions?.length > 0 && (
                                      selectedTaskIssue.task.conditions
                                        ?.filter((condition) => condition.source === question.attribute)
                                        .map((condition) => (
                                          <div key={condition.id} className="mb-3">
                                            <p>{gettext('YOUR ANSWER:')} {condition.relation_label} {' '}
                                              {condition.target_option_text || condition.target_text}</p>
                                          </div>
                                        ))
                                    )
                                  }
                                </div>
                              ))
                            }
                          </>
                        )
                      }
                    </div>

                    {
                      selectedTaskIssue.dates?.length > 0 && (
                        <div className="col-md-4">
                          <>
                            <div className="fw-bold mb-2">{gettext('Dates')}</div>

                            {
                              selectedTaskIssue.dates.map((date, index) => (
                                <div key={index} className="mb-2">
                                  {renderDate(date)}
                                </div>
                              ))
                            }
                          </>
                        </div>
                      )
                    }
                  </div>
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
