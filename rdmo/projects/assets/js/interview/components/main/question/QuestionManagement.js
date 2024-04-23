import React from 'react'
import PropTypes from 'prop-types'

import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'

const QuestionManagement = ({ question }) => {
  return (
    <div className="well well-sm">
      <ul className="list-unstyled mb-0">
        <li>
          <a href={`${baseUrl}/management/questions/${question.id}/`} target="_blank" rel="noreferrer">
            <code className="code-questions">{question.uri}</code>
          </a>
        </li>
        <li>
          <a href={`${baseUrl}/management/attributes/${question._attribute.id}/`} target="_blank" rel="noreferrer">
            <code className="code-attributes">{question._attribute.uri}</code>
          </a>
        </li>
      </ul>
    </div>
  )
}

QuestionManagement.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionManagement
