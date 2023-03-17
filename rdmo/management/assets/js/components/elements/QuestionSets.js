import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import QuestionSet from '../element/QuestionSet'
import ElementButtons from '../common/ElementButtons'

const QuestionSets = ({ config, questionsets, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <strong>{gettext('Question sets')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, questionsets).map((questionset, index) => (
          <QuestionSet key={index} config={config} questionset={questionset}
                       fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

QuestionSets.propTypes = {
  config: PropTypes.object.isRequired,
  questionsets: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default QuestionSets
