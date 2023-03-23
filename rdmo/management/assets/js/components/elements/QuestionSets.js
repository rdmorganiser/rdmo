import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements, getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import QuestionSet from '../element/QuestionSet'
import { BackButton, NewButton } from '../common/ElementButtons'

const QuestionSets = ({ config, questionsets, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.questionsets.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.questionsets.uriPrefix', uriPrefix)

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

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterUri value={config.filter.questionsets.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter questionsets by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.questionsets.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(questionsets)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        filterElements(config.filter.questionsets, questionsets).map((questionset, index) => (
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
