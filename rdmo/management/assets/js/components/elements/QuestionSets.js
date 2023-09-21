import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import QuestionSet from '../element/QuestionSet'

const QuestionSets = ({ config, questionsets, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.questionsets.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.questionsets.uri_prefix', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.editors', value)

  const updateDisplayQuestionSetsURI = (value) => configActions.updateConfig('display.uri.questionsets', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)
  const updateDisplayConditionsURI = (value) => configActions.updateConfig('display.uri.conditions', value)

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
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.questionsets.search', '')} onChange={updateFilterString}
                          placeholder={gettext('Filter question sets')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.questionsets.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(questionsets)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                          options={config.sites} allLabel={gettext('All editors')} />
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
                       configActions={configActions} elementActions={elementActions}
                       filter="questionsets" filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

QuestionSets.propTypes = {
  config: PropTypes.object.isRequired,
  questionsets: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default QuestionSets
