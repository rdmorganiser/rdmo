import React from 'react'
import PropTypes from 'prop-types'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { managementHelp } from '../../../constants/management'

const QuestionSetManagement = ({ config, questionset, isManager }) => {
  return config.showManagement && isManager && (
    <div className="panel panel-default interview-management">
      <div className="panel-body">
        <div className="interview-management-help" title={managementHelp}>
          <i className="fa fa-question-circle-o" aria-hidden="true"></i>
        </div>
        <ul className="list-unstyled mb-0">
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
  config: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  isManager: PropTypes.bool.isRequired,
}

export default QuestionSetManagement
