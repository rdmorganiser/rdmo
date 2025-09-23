import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import QuestionSet from '../element/QuestionSet'

const QuestionSets = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const questionsets = useSelector((state) => state.elements.questionsets)

  const updateFilterString = (value) => dispatch(updateConfig('filter.questionsets.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.questionsets.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const updateDisplayQuestionSetsURI = (value) => dispatch(updateConfig('display.uri.questionsets', value))
  const updateDisplayAttributesURI = (value) => dispatch(updateConfig('display.uri.attributes', value))
  const updateDisplayConditionsURI = (value) => dispatch(updateConfig('display.uri.conditions', value))

  const createQuestionSet = () => dispatch(createElement('questionsets'))

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
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.questionsets.search', '')} onChange={updateFilterString}
                          label={gettext('Filter question sets')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.questionsets.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(questionsets)} />
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
          <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                    value={get(config, 'display.uri.questionsets', true)} onChange={updateDisplayQuestionSetsURI} />
          <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                    value={get(config, 'display.uri.attributes', true)} onChange={updateDisplayAttributesURI} />
          <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                    value={get(config, 'display.uri.conditions', true)} onChange={updateDisplayConditionsURI} />
        </div>
      </div>

      <ul className="list-group">
      {
        questionsets.map((questionset, index) => (
          <QuestionSet key={index} config={config} questionset={questionset}
                       filter="questionsets" filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

export default QuestionSets
