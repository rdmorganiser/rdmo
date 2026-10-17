import React from 'react'
import { useSelector } from 'react-redux'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import Tooltip from 'rdmo/core/assets/js/components/Tooltip'

import { usePermissions } from '../../../../../hooks'

const PageManagement = () => {
  const config = useSelector((state) => state.config)
  const templates = useSelector((state) => state.templates)
  const page = useSelector((state) => state.interview.page)
  const perms = usePermissions()

  return config.showManagement && perms.can_view_management && (
    <div className="project-interview-management mb-2">
      <div className="border p-2 rounded-2">
        <div className="float-end">
          <Tooltip title={templates.project_interview_management_help} placement="bottom">
            <i className="bi bi-info-circle text-muted cursor-help" tabIndex={0} />
          </Tooltip>
        </div>

        <ul className="d-flex flex-column gap-1 list-unstyled mb-0">
          <li>
            <a href={`${baseUrl}/management/pages/${page.id}/`} target="_blank" rel="noreferrer">
              <code className="code-questions">{page.uri}</code>
            </a>
          </li>
          {
            page.attribute && (
              <li>
                <a href={`${baseUrl}/management/attributes/${page.attribute}/`} target="_blank" rel="noreferrer">
                  <code className="code-domain">{page.attribute_uri}</code>
                </a>
              </li>
            )
          }
          {
            page.conditions.map((condition, conditionIndex) => (
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

export default PageManagement
