import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import QuestionSet from '../element/QuestionSet'
import Question from '../element/Question'
import { BackButton } from '../common/ElementButtons'

const NestedQuestionSet = ({ config, questionset, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.questionset.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.questionset.uriPrefix', uriPrefix)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <QuestionSet config={config} questionset={questionset}
                       elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterUri value={config.filter.questionset.uri} onChange={updateFilterUri}
                         placeholder={gettext('Filter question sets by URI')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.questionset.uriPrefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(questionset.elements)} />
            </div>
          </div>
        </div>
      </div>

      {
        questionset.elements.map((element, index) => {
          if (isUndefined(element.text)) {
            return <QuestionSet key={index} config={config} questionset={element} elementActions={elementActions}
                                display="nested" filter={config.filter.questionset} indent={1} />
          } else {
            return <Question key={index} config={config} question={element} elementActions={elementActions}
                             display="nested" filter={config.filter.questionset} indent={1} />
          }
        })
      }
    </>
  )
}

NestedQuestionSet.propTypes = {
  config: PropTypes.object.isRequired,
  questionset: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedQuestionSet
