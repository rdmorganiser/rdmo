import React from 'react'
import PropTypes from 'prop-types'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import { useFormattedDateTime } from 'rdmo/core/assets/js/hooks'
import { language } from 'rdmo/core/assets/js/utils'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import Select from 'rdmo/core/assets/js/components/forms/Select'

import { projectId } from '../../../utils/meta'

const IssueModal = ({
  canChangeIssue = false,
  issue,
  onClose,
  onStatusChange,
}) => {

  const statusOptions = [
    { value: 'open', label: gettext('Open') },
    { value: 'closed', label: gettext('Closed') },
    { value: 'in_progress', label: gettext('In progress') },
  ]

  const renderDate = (date) => (
    date.map((dateValue) => useFormattedDateTime(dateValue, language, 'dateOnly')).join(' - ')
  )

  return (
    <Modal
      show
      title={issue.task.title}
      onClose={onClose}
      size="modal-lg"
      closeLabel={gettext('Close')}
    >
      <p>{issue.task.text}</p>
      <Select
        isDisabled={!canChangeIssue}
        label={gettext('Status')}
        options={statusOptions}
        value={issue.status}
        onChange={onStatusChange}
      />
      <div className="row mt-3">
        <div className={issue.dates?.length > 0 ? 'col-md-8' : 'col-md-12'}>
          {/* questions */}
          {
            issue.questions?.length > 0 && (
              <>
                <div className="fw-bold mb-2">{gettext('Why is this task shown?')}</div>
                <p>{gettext('This task is shown based on your answers:')}</p>
                {
                  issue.questions.map((question) => (
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
                        issue.task.conditions?.length > 0 && (
                          issue.task.conditions
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
          issue.dates?.length > 0 && (
            <div className="col-md-4">
              <div className="fw-bold mb-2">{gettext('Dates')}</div>

              {
                issue.dates.map((date, index) => (
                  <div key={index} className="mb-2">
                    {renderDate(date)}
                  </div>
                ))
              }
            </div>
          )
        }
      </div>
    </Modal>
  )
}

IssueModal.propTypes = {
  canChangeIssue: PropTypes.bool,
  issue: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired,
  onStatusChange: PropTypes.func.isRequired,
}

export default IssueModal
