import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import QuestionSet from '../element/QuestionSet'
import { BackButton, NewButton } from '../common/ElementButtons'

const QuestionSets = ({ config, questionsets, elementActions }) => {

  const createQuestionSet = () => elementActions.createElement('questionsets')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createQuestionSet} />
        </div>
        <strong>{gettext('Question sets')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, questionsets).map((questionset, index) => (
          <QuestionSet key={index} config={config} questionset={questionset}
                       elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

QuestionSets.propTypes = {
  config: PropTypes.object.isRequired,
  questionsets: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default QuestionSets
