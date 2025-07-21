import React from 'react'
import PropTypes from 'prop-types'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { managementHelp } from '../../../constants/management'

const PageManagement = ({ config, page, isManager }) => {
  return config.showManagement && isManager && (
    <div className="panel panel-default interview-management">
      <div className="panel-body">
        <div className="interview-management-help" title={managementHelp}>
          <i className="fa fa-question-circle-o" aria-hidden="true"></i>
        </div>
        <ul className="list-unstyled mb-0">
          <li>
            <a href={`${baseUrl}/management/pages/${page.id}/`} target="_blank" rel="noreferrer">
              <code className="code-questions">{page.uri}</code>
            </a>
          </li>
          {
            page.attribute && (
              <li>
                <a href={`${baseUrl}/management/attributes/${page.attribute}/`} target="_blank" rel="noreferrer">
                  <code className="code-attributes">{page.attribute_uri}</code>
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

PageManagement.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  isManager: PropTypes.bool.isRequired,
}

export default PageManagement
