import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton } from '../common/Buttons'
import { Drop } from '../common/DragAndDrop'

import QuestionSet from '../element/QuestionSet'
import Question from '../element/Question'

const NestedQuestionSet = ({ config, questionset, configActions, elementActions }) => {

  const updateFilterString = (uri) => configActions.updateConfig('filter.questionset.search', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.questionset.uri_prefix', uriPrefix)

  const updateDisplayQuestionSets = (value) => configActions.updateConfig('display.elements.questionsets', value)
  const updateDisplayQuestions = (value) => configActions.updateConfig('display.elements.questions', value)
  const updateDisplayQuestionsURI = (value) => configActions.updateConfig('display.uri.questions', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)

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
              <FilterString value={config.filter.questionset.search} onChange={updateFilterString}
                            placeholder={gettext('Filter question sets')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.questionset.uri_prefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(questionset.elements)} />
            </div>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show elements:')}</span>
            <Checkbox label={gettext('Question sets')} value={config.display.elements.questionsets} onChange={updateDisplayQuestionSets} />
            <Checkbox label={gettext('Questions')} value={config.display.elements.questions} onChange={updateDisplayQuestions} />
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                      value={config.display.uri.questions} onChange={updateDisplayQuestionsURI} />
            <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                      value={config.display.uri.attributes} onChange={updateDisplayAttributesURI} />
          </div>
        </div>
      </div>
      {
        !isEmpty(questionset.elements) &&
        <Drop element={questionset.elements[0]} elementActions={elementActions} indent={1} mode="before" />
      }
      {
        questionset.elements.map((element, index) => {
          if (element.model == 'questions.questionset') {
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
