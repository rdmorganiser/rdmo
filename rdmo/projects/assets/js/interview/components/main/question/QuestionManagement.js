import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

const QuestionManagement = ({ question, isManager }) => {
  return isManager && (
    <ul className="list-unstyled">
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
  )
}

QuestionManagement.propTypes = {
  question: PropTypes.object.isRequired,
  isManager: PropTypes.bool.isRequired,
}

export default QuestionManagement
