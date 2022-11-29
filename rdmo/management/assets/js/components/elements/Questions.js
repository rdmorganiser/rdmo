import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

const Questions = ({ config, questions }) => {
  return (
    <div className="questions">
      <div className="panel panel-default">
        <div className="panel-body">
          <strong>Questions</strong>
        </div>
      </div>
      {
        filterElements(config, questions).map((question, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
                <strong>Question</strong> {question.text}
              </div>
              <div className="panel-body">
                <code className="code-questions">{question.uri}</code>
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

Questions.propTypes = {
  questions: PropTypes.array.isRequired
}

export default Questions
