import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import { Html, Tooltip } from 'rdmo/core/assets/js/components'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { usePermissions } from '../../../../../hooks'

const QuestionSetManagement = ({ questionset }) => {
  const config = useSelector((state) => state.config)
  const templates = useSelector((state) => state.templates)
  const perms = usePermissions()

  return config.showManagement && perms.can_view_management && (
    <div className="project-interview-management mb-2">
      <div className="border p-2 rounded-2">
        <div className="float-end">
          <Tooltip title={<Html html={templates.project_interview_management_help} />} placement="bottom">
            <i className="bi bi-info-circle text-muted cursor-help" tabIndex={0} />
          </Tooltip>
        </div>

        <ul className="d-flex flex-column gap-1 list-unstyled mb-0">
          <li>
            <a href={`${baseUrl}/management/questionsets/${questionset.id}/`} target="_blank" rel="noreferrer">
              <code className="code-questions">{questionset.uri}</code>
            </a>
          </li>
          {
            questionset.conditions.map((condition, conditionIndex) => (
              <li key={conditionIndex}>
                <a href={`${baseUrl}/management/conditions/${condition.id}/`} target="_blank" rel="noreferrer">
                  <code className="code-conditions">{condition.uri}</code>
                </a>
              </li>
            ))
          }
        </ul>
      </div>
    </div>
  )
}

QuestionSetManagement.propTypes = {
  questionset: PropTypes.object.isRequired
}

export default QuestionSetManagement
