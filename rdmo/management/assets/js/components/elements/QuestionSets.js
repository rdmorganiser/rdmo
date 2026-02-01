import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import QuestionSet from '../element/QuestionSet'

const QuestionSets = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const questionsets = useSelector((state) => state.elements.questionsets)

  const updateFilterString = (value) => dispatch(updateConfig('filter.questionsets.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.questionsets.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const displayUriQuestionSets = isTruthy(get(config, 'display.uri.questionsets', true))
  const displayUriAttributes = isTruthy(get(config, 'display.uri.attributes', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))

  const toggleDisplayUriQuestionSets = () => dispatch(updateConfig('display.uri.questionsets', !displayUriQuestionSets))
  const toggleDisplayUriAttributes = () => dispatch(updateConfig('display.uri.attributes', !displayUriAttributes))
  const toggleDisplayUriConditions = () => dispatch(updateConfig('display.uri.conditions', !displayUriConditions))

  const createQuestionSet = () => dispatch(createElement('questionsets'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Question sets')}</strong>
          <BackButton />
          <NewButton onClick={createQuestionSet} />
        </div>
      </div>

      <div className="card-body">
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
        <div className="input-group input-group-sm mb-2">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={toggleDisplayUriQuestionSets} className={btnClass(displayUriQuestionSets)}>
            {gettext('Question sets')}
          </button>
          <button type="button" onClick={toggleDisplayUriAttributes} className={btnClass(displayUriAttributes)}>
            {gettext('Attributes')}
          </button>
          <button type="button" onClick={toggleDisplayUriConditions} className={btnClass(displayUriConditions)}>
            {gettext('Conditions')}
          </button>
        </div>
      </div>

      {
        !isEmpty(questionsets) && (
          <ul className="list-group list-group-flush">
          {
            questionsets.map((questionset, index) => (
              <QuestionSet key={index} config={config} questionset={questionset}
                           filter="questionsets" filterEditors={true} />
            ))
          }
          </ul>

        )
      }
    </div>
  )
}

export default QuestionSets
