import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { filterElements } from '../../utils/filter'

import QuestionSet from '../element/QuestionSet'
import Question from '../element/Question'
import { BackButton } from '../common/ElementButtons'

const NestedQuestionSet = ({ config, questionset, elementActions }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
        </div>
        <QuestionSet config={config} questionset={questionset}
                     elementActions={elementActions} list={false} />
      </div>

      <ul className="list-group">
      {
        filterElements(config, questionset.elements).map((element, index) => {
          if (isUndefined(element.text)) {
            return <QuestionSet key={index} config={config} questionset={element}
                                elementActions={elementActions} />
          } else {
            return <Question key={index} config={config} question={element}
                             elementActions={elementActions} />
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
  elementActions: PropTypes.object.isRequired
}

export default NestedQuestionSet
