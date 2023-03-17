import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Question from '../element/Question'
import ElementButtons from '../common/ElementButtons'

const Questions = ({ config, questions, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <strong>{gettext('Questions')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, questions).map((question, index) => (
          <Question key={index} config={config} question={question}
                    fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Questions.propTypes = {
  config: PropTypes.object.isRequired,
  questions: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Questions
