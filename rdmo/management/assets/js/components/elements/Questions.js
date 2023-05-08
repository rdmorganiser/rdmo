import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Question from '../element/Question'

const Questions = ({ config, questions, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.questions.string', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.questions.uriPrefix', value)
  const updateDisplayQuestionsURI = (value) => configActions.updateConfig('display.uri.questions', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)

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
            <FilterString value={config.filter.questions.string} onChange={updateFilterString}
                          placeholder={gettext('Filter questions')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.questions.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(questions)} />
          </div>
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                    value={config.display.uri.questions} onChange={updateDisplayQuestionsURI} />
          <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                    value={config.display.uri.attributes} onChange={updateDisplayAttributesURI} />
        </div>
      </div>

      <ul className="list-group">
      {
        questions.map((question, index) => (
          <Question key={index} config={config} question={question} elementActions={elementActions}
                    filter={config.filter.questions} />
        ))
      }
      </ul>
    </div>
  )
}

Questions.propTypes = {
  config: PropTypes.object.isRequired,
  questions: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Questions
