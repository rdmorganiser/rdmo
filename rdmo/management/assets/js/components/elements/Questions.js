import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements, getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Question from '../element/Question'
import { BackButton, NewButton } from '../common/ElementButtons'

const Questions = ({ config, questions, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.questions.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.questions.uriPrefix', uriPrefix)

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

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterUri value={config.filter.questions.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter questions by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.questions.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(questions)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        filterElements(config.filter.questions, questions).map((question, index) => (
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
