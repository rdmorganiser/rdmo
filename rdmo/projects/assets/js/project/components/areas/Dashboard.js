import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'

import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import { LinkButton } from 'rdmo/core/assets/js/components'

import { navigateDashboard } from '../../actions/navigationActions'
import { updateProjectTask } from '../../actions/projectActions'
import { usePermissions } from '../../hooks'
import { IssueTile } from '../helper'

import IssueDate from '../../../common/components/IssueDate'

import IssueModal from './dashboard/IssueModal'
import SendIssueModal from './dashboard/SendIssueModal'
import ShowClosedIssues from './dashboard/ShowClosedIssues'

const Dashboard = () => {
  const dispatch = useDispatch()
  const config = useSelector(state => state.config)
  const settings = useSelector(state => state.settings)
  const perms = usePermissions()

  const allIssues = useSelector((state) => state.project.project.tasks) ?? []
  /* Show only issues that resolve */
  const issues = allIssues.filter((issue) => issue.resolve === true)

  const { showClosedTasks, showClosedRecommendations } = config

  const [selectedIssue, setSelectedIssue] = useState(null)
  const [sendIssue, setSendIssue] = useState(null)

  const isClosed = (issue) => issue.status === 'closed'
  const getTaskType = (issue) => issue.task?.task_type

  const stepIssues = issues.filter((issue) =>
    getTaskType(issue) === 'step'
  ).sort((a, b) => a.task.order - b.task.order)

  const activeStepIssue = stepIssues.find((issue) => !isClosed(issue))

  // we need these 2 constants to avoid losing the toggle switch if all issues are closed (but not visible)
  const taskIssues = issues.filter((issue) => getTaskType(issue) === 'task')
  const recommendationIssues = issues.filter((issue) => getTaskType(issue) === 'recommendation')

  const visibleTaskIssues = taskIssues
    .filter((issue) => showClosedTasks || !isClosed(issue))
    .sort((a, b) => Number(isClosed(a)) - Number(isClosed(b)))

  const visibleRecommendationIssues = recommendationIssues
    .filter((issue) => showClosedRecommendations || !isClosed(issue))
    .sort((a, b) => Number(isClosed(a)) - Number(isClosed(b)))

  const guidanceIssues = issues.filter((issue) =>
    getTaskType(issue) === 'guidance'
  ).sort((a, b) => a.task.order - b.task.order)

  const toggleTaskDone = (issueId, currentStatus) => {
    dispatch(updateProjectTask(issueId, {
      status: currentStatus === 'closed' ? 'open' : 'closed'
    }))
  }

  const renderVisibleIssue = (issue) => {
    const closed = isClosed(issue)
    const disabled = !perms.can_change_issue
    const resourceCount = issue.resources?.length ?? 0
    return (
      <div className="d-flex align-items-start gap-3">
        <div>
          <LinkButton
            title={closed ? gettext('Mark task as not done') : gettext('Mark task as done')}
            disabled={disabled}
            onClick={() => toggleTaskDone(issue.id, issue.status)}
          >
            <i className={
              classNames('bi', {
                'bi-check-circle-fill': closed,
                'bi-circle': !closed,
                'text-muted': disabled
              })
            } />
          </LinkButton>
        </div>

        <div className="flex-grow-1">
          <div className="d-flex justify-content-between align-items-start">
            <strong className={classNames('mb-3', {'text-muted': closed})}>
              {issue.task.title}
            </strong>
            {
              canSendIssue(issue) && (
                <LinkButton
                  title={gettext('Send task')}
                  onClick={() => setSendIssue(issue)}
                >
                  <i className="bi bi-send" aria-hidden="true" />
                </LinkButton>
              )
            }
          </div>

          <p className="text-secondary">{issue.task.text}</p>
          {
            resourceCount > 0 && (
              <div className="text-muted small mt-2">
                <i className="bi bi-box-arrow-up-right me-1" />
                {
                  interpolate(ngettext(
                    '%s external resource',
                    '%s external resources',
                    resourceCount
                  ), [resourceCount])
                }
              </div>
            )
          }
          {
            issue.dates?.length > 0 && (
              <div className="text-muted small mt-2 text-end">
                <i className="bi bi-clock me-1" />
                <IssueDate date={issue.dates[0]} />
              </div>
            )
          }
        </div>
      </div>
    )
  }

  return (
    <div>
      <h1 className="mb-5">{gettext('Dashboard')}</h1>

      {
        perms.can_view_issue && (
          <>
            {
              stepIssues.length > 0 && (
                <div className="project-dashboard-steps mb-4">
                  <h2>{gettext('Create your data management plan')}</h2>
                  <div className="row">
                    {
                      stepIssues.map((issue, index) => {
                        const isActiveStep = activeStepIssue?.id === issue.id
                        return (
                          <IssueTile
                            key={issue.id}
                            className="col-lg-6 mb-4"
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
                            <p className="text-secondary">{issue.task.text}</p>
                          </IssueTile>
                        )
                      })
                    }
                  </div>
                </div>
              )
            }
            {
              taskIssues.length > 0 && (
                <div className="project-dashboard-tasks mb-4">
                  <h2>{gettext('Tasks')}</h2>
                  <ShowClosedIssues
                    id="showClosedTasks"
                    label={gettext('Show closed tasks')}
                    checked={showClosedTasks}
                    onChange={() => dispatch(configActions.updateConfig('showClosedTasks', !showClosedTasks))}
                  />
                  <div className="row">
                    {
                      visibleTaskIssues.map((issue) => (
                        <IssueTile
                          key={issue.id}
                          className="col-lg-6 mb-4"
                          onCardClick={() => setSelectedIssue(issue)}
                        >
                          {renderVisibleIssue(issue)}
                        </IssueTile>
                      ))
                    }
                  </div>
                </div>
              )
            }
            {
              recommendationIssues.length > 0 && (
                <div className="project-dashboard-recommendations mb-4">
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
                  <div className="row">
                    {
                      visibleRecommendationIssues.map((issue) => (
                        <IssueTile
                          key={issue.id}
                          className="col-lg-6 mb-4"
                          onCardClick={() => setSelectedIssue(issue)}
                        >
                          {renderVisibleIssue(issue)}
                        </IssueTile>
                      ))
                    }
                  </div>
                </div>
              )
            }
            {
              guidanceIssues.length > 0 && (
                <div className="project-dashboard-guidance mb-4">
                  <h2>{gettext('More actions')}</h2>
                  <div className="row">
                    {
                      guidanceIssues.map((issue) => (
                        <IssueTile
                          key={issue.id}
                          className="col-lg-4 mb-4"
                          title={issue.task.title}
                          buttonLabel={issue.task.task_area_display}
                          buttonIconClassName="bi bi-arrow-right"
                          onClick={
                            issue.task.task_area ? (
                              () => dispatch(navigateDashboard({ area: issue.task.task_area }))
                            ) : undefined
                          }
                        >
                          <p className="text-secondary">{issue.task.text}</p>
                        </IssueTile>
                      ))
                    }
                  </div>
                </div>
              )
            }
            {
              selectedIssue && (
                <IssueModal
                  canChangeIssue={perms.can_change_issue}
                  canSendIssue={canSendIssue(selectedIssue)}
                  issue={selectedIssue}
                  onClose={() => setSelectedIssue(null)}
                  onSend={() => handleSendIssue(selectedIssue)}
                  onStatusChange={
                    (status) => {
                      dispatch(updateProjectTask(selectedIssue.id, { status }))
                      setSelectedIssue({
                        ...selectedIssue,
                        status,
                      })
                    }
                  }
                />
              )
            }
            {
              sendIssue && (
                <SendIssueModal
                  onClose={() => setSendIssue(null)}
                  issue={sendIssue}
                />
              )
            }
          </>
        )
      }
    </div>
  )
}

export default Dashboard
