import React, { Component } from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Page from '../element/Page'
import QuestionSet from '../element/QuestionSet'
import Question from '../element/Question'
import { Checkbox } from '../common/Checkboxes'
import { BackButton } from '../common/Buttons'

const NestedPage = ({ config, page, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.page.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.page.uriPrefix', uriPrefix)

  const updateDisplayQuestionSets = (value) => configActions.updateConfig('display.elements.questionsets', value)
  const updateDisplayQuestions = (value) => configActions.updateConfig('display.elements.questions', value)
  const updateDisplayQuestionSetsURI = (value) => configActions.updateConfig('display.uri.questionsets', value)
  const updateDisplayQuestionsURI = (value) => configActions.updateConfig('display.uri.questions', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Page config={config} page={page}
                elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterUri value={config.filter.page.uri} onChange={updateFilterUri}
                         placeholder={gettext('Filter pages by URI')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.page.uriPrefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(page.elements)} />
            </div>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show elements:')}</span>
            <Checkbox label={gettext('Question sets')} value={config.display.elements.questionsets} onChange={updateDisplayQuestionSets} />
            <Checkbox label={gettext('Questions')} value={config.display.elements.questions} onChange={updateDisplayQuestions} />
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                      value={config.display.uri.questionsets} onChange={updateDisplayQuestionSetsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                      value={config.display.uri.questions} onChange={updateDisplayQuestionsURI} />
            <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                      value={config.display.uri.attributes} onChange={updateDisplayAttributesURI} />
          </div>
        </div>
      </div>

      {
        page.elements.map((element, index) => {
          if (isUndefined(element.text)) {
            return <QuestionSet key={index} config={config} questionset={element} elementActions={elementActions}
                                display="nested" filter={config.filter.page} indent={1} />
          } else {
            return <Question key={index} config={config} question={element} elementActions={elementActions}
                             display="nested" filter={config.filter.page} indent={1} />
          }
        })
      }
    </>
  )
}

NestedPage.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedPage
