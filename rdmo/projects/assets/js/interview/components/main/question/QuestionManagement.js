import React from 'react'
import PropTypes from 'prop-types'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { managementHelp } from '../../../constants/management'

const QuestionManagement = ({ config, question, isManager }) => {
  return config.showManagement && isManager && (
    <div className="panel panel-default interview-management">
      <div className="panel-body">
        <div className="interview-management-help" title={managementHelp}>
          <i className="fa fa-question-circle-o" aria-hidden="true"></i>
        </div>
        <ul className="list-unstyled mb-0">
          <li>
            <a href={`${baseUrl}/management/questions/${question.id}/`} target="_blank" rel="noreferrer">
              <code className="code-questions">{question.uri}</code>
            </a>
          </li>
          <li>
            <a href={`${baseUrl}/management/attributes/${question.attribute}/`} target="_blank" rel="noreferrer">
              <code className="code-attributes">{question.attribute_uri}</code>
            </a>
          </li>
          {
            question.optionsets.map((optionset, optionsetIndex) => (
              <li key={optionsetIndex}>
                <a href={`${baseUrl}/management/optionsets/${optionset.id}/`} target="_blank" rel="noreferrer">
                  <code className="code-options">{optionset.uri}</code>
                </a>
              </li>
            ))
          }
          {
            question.conditions.map((condition, conditionIndex) => (
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

QuestionManagement.propTypes = {
  config: PropTypes.object.isRequired,
  question: PropTypes.object.isRequired,
  isManager: PropTypes.bool.isRequired,
}

export default QuestionManagement
