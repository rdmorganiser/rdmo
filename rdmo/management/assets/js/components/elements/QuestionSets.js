import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

const QuestionSets = ({ config, questionsets }) => {
  return (
    <div className="questionsets">
      <div className="panel panel-default">
        <div className="panel-body">
          <strong>Question sets</strong>
        </div>
      </div>
      {
        filterElements(config, questionsets).map((questionset, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
                <strong>Question set</strong> {questionset.title}
              </div>
              <div className="panel-body">
                <code className="code-questions">{questionset.uri}</code>
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

QuestionSets.propTypes = {
  questionsets: PropTypes.array.isRequired
}

export default QuestionSets
