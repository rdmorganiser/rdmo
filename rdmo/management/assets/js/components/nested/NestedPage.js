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

import Page from '../element/Page'
import QuestionSet from '../element/QuestionSet'
import Question from '../element/Question'

const NestedPage = ({ config, page, configActions, elementActions }) => {

  const updateFilterString = (uri) => configActions.updateConfig('filter.page.search', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.page.uri_prefix', uriPrefix)

  const toggleQuestionSets = () => elementActions.toggleDescendants(page, 'questionsets')

  const updateDisplayPagesURI = (value) => configActions.updateConfig('display.uri.pages', value)
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
          <Page config={config} page={page}
                configActions={configActions} elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={get(config, 'filter.page.search', '')} onChange={updateFilterString}
                            placeholder={gettext('Filter pages')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={get(config, 'filter.page.uri_prefix', '')} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(page.elements)} />
            </div>
          </div>
          <div className="mt-10">
            <span className="mr-10">{gettext('Show elements:')}</span>
            <Link className="mr-10" onClick={toggleQuestionSets}>{gettext('Question sets')}</Link>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Pages')}</code>}
                      value={get(config, 'config.display.uri.pages', true)} onChange={updateDisplayPagesURI} />
            <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                      value={get(config, 'config.display.uri.questionsets', true)} onChange={updateDisplayQuestionSetsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                      value={get(config, 'config.display.uri.questions', true)} onChange={updateDisplayQuestionsURI} />
            <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                      value={get(config, 'config.display.uri.attributes', true)} onChange={updateDisplayAttributesURI} />
            <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                      value={get(config, 'config.display.uri.conditions', true)} onChange={updateDisplayConditionsURI} />
            <Checkbox label={<code className="code-options">{gettext('Option sets')}</code>}
                      value={get(config, 'config.display.uri.optionsets', true)} onChange={updateDisplayOptionSetURI} />
          </div>
        </div>
      </div>
      {
        !isEmpty(page.elements) &&
        <Drop element={page.elements[0]} elementActions={elementActions} indent={1} mode="before" />
      }
      {
        page.elements.map((element, index) => {
          if (element.model == 'questions.questionset') {
            return <QuestionSet key={index} config={config} questionset={element}
                                configActions={configActions} elementActions={elementActions}
                                display="nested" filter="page" indent={1} />
          } else {
            return <Question key={index} config={config} question={element}
                             configActions={configActions} elementActions={elementActions}
                             display="nested" filter="page" indent={1} />
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
