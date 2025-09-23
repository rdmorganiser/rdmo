import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Question from '../element/Question'

const Questions = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const questions = useSelector((state) => state.elements.questions)

  const updateFilterString = (value) => dispatch(updateConfig('filter.questions.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.questions.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const updateDisplayQuestionsURI = (value) => dispatch(updateConfig('display.uri.questions', value))
  const updateDisplayAttributesURI = (value) => dispatch(updateConfig('display.uri.attributes', value))
  const updateDisplayConditionsURI = (value) => dispatch(updateConfig('display.uri.conditions', value))
  const updateDisplayOptionSetURI = (value) => dispatch(updateConfig('display.uri.optionsets', value))

  const createQuestion = () => dispatch(createElement('questions'))

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
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.questions.search', '')} onChange={updateFilterString}
                          label={gettext('Filter questions')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.questions.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(questions)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                          options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
            </div>
          }
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
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

      <ul className="list-group">
      {
        questions.map((question, index) => (
          <Question key={index} config={config} question={question}
                    filter="questions" filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

export default Questions
