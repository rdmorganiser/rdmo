import React from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import QuestionSet from '../element/QuestionSet'

const QuestionSets = ({ config, questionsets, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.questionsets.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.questionsets.uri_prefix', value)

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
          <div className="col-sm-8">
            <FilterString value={config.filter.questionsets.search} onChange={updateFilterString}
                          placeholder={gettext('Filter question sets')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.questionsets.uri_prefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(questionsets)} />
          </div>
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                    value={config.display.uri.questionsets} onChange={updateDisplayQuestionSetsURI} />
          <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                    value={config.display.uri.attributes} onChange={updateDisplayAttributesURI} />
          <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                    value={config.display.uri.conditions} onChange={updateDisplayConditionsURI} />
        </div>
      </div>

      <ul className="list-group">
      {
        questionsets.map((questionset, index) => (
          <QuestionSet key={index} config={config} questionset={questionset} elementActions={elementActions}
                       filter={config.filter.questionsets} />
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
