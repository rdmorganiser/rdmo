import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'

import Link from 'rdmo/core/assets/js/components/Link'

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

  const toggleQuestionSets = () => configActions.toggleDescendants(questionset, 'questionsets')

  const updateDisplayQuestionSetsURI = (value) => configActions.updateConfig('display.uri.questionsets', value)
  const updateDisplayQuestionsURI = (value) => configActions.updateConfig('display.uri.questions', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)
  const updateDisplayConditionsURI = (value) => configActions.updateConfig('display.uri.conditions', value)
  const updateDisplayOptionSetURI = (value) => configActions.updateConfig('display.uri.optionsets', value)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <QuestionSet config={config} questionset={questionset}
                       configActions={configActions} elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={get(config, 'filter.questionset.search', '')} onChange={updateFilterString}
                            placeholder={gettext('Filter question sets')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={get(config, 'filter.questionset.uri_prefix', '')} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(questionset.elements)} />
            </div>
          </div>
          <div className="mt-10">
            <span className="mr-10">{gettext('Show elements:')}</span>
            <Link className="mr-10" onClick={toggleQuestionSets}>{gettext('Question sets')}</Link>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                      value={get(config, 'display.uri.questionsets', true)} onChange={updateDisplayQuestionSetsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                      value={get(config, 'display.uri.questions', true)} onChange={updateDisplayQuestionsURI} />
            <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                      value={get(config, 'display.uri.attributes', true)} onChange={updateDisplayAttributesURI} />
            <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                      value={get(config, 'display.uri.conditions', true)} onChange={updateDisplayConditionsURI} />
            <Checkbox label={<code className="code-options">{gettext('Option sets')}</code>}
                      value={get(config, 'display.uri.optionsets', true)} onChange={updateDisplayOptionSetURI} />
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
            return <QuestionSet key={index} config={config} questionset={element}
                                configActions={configActions} elementActions={elementActions}
                                display="nested" filter="questionset" indent={1} />
          } else {
            return <Question key={index} config={config} question={element}
                             configActions={configActions} elementActions={elementActions}
                             display="nested" filter="questionset" indent={1} />
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
