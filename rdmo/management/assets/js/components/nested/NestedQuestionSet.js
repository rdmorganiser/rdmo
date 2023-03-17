import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElements } from '../../utils/filter'

import QuestionSet from '../element/QuestionSet'
import Question from '../element/Question'
import ElementButtons from '../common/ElementButtons'

const NestedQuestionSet = ({ config, questionset, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <QuestionSet config={config} questionset={questionset}
                     fetchElement={fetchElement} storeElement={storeElement} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, questionset.elements).map((element, index) => {
          if (isUndefined(element.text)) {
            return <QuestionSet key={index} config={config} questionset={element}
                                fetchElement={fetchElement} storeElement={storeElement} />
          } else {
            return <Question key={index} config={config} question={element}
                             fetchElement={fetchElement} storeElement={storeElement} />
          }
        })
      }
      </ul>
    </div>
  )
}

NestedQuestionSet.propTypes = {
  config: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default NestedQuestionSet
