import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Questions = ({ questions }) => {
  return (
    <div className="questions">
      <div className="panel panel-default">
        <div className="panel-body">
          <strong>Questions</strong>
        </div>
      </div>
      {
        questions.map((question, index) => {
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
