import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Question from '../element/Question'
import { BackButton, NewButton } from '../common/ElementButtons'

const Questions = ({ config, questions, elementActions }) => {

  const createQuestion = () => elementActions.createElement('questions')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createQuestion} />
        </div>
        <strong>{gettext('Questions')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, questions).map((question, index) => (
          <Question key={index} config={config} question={question}
                    elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Questions.propTypes = {
  config: PropTypes.object.isRequired,
  questions: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Questions
