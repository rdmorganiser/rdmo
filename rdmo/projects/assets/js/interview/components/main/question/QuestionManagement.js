import React from 'react'
import PropTypes from 'prop-types'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

const QuestionManagement = ({ config, question, isManager }) => {
  const help = gettext('These links take you directly to the items in the admin interface. ' +
                       ' This part of the page is visible to you because you are either an Admin, ' +
                       ' Editor, or Reviewer. It is not displayed for regular users. It can be disabled' +
                       ' in the sidebar.')

  return config.showManagement && isManager && (
    <div className="panel panel-default interview-management">
      <div className="panel-body">
        <div className="interview-management-help"
                title={help}>
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
