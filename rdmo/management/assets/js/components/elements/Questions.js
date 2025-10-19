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

import Question from '../element/Question'

const Questions = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const questions = useSelector((state) => state.elements.questions)

  const updateFilterString = (value) => dispatch(updateConfig('filter.questions.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.questions.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const displayUriQuestions = isTruthy(get(config, 'display.uri.questions', true))
  const displayUriAttributes = isTruthy(get(config, 'display.uri.attributes', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))
  const displayUriOptionSets = isTruthy(get(config, 'display.uri.optionsets', true))

  const updateDisplayQuestionsURI = () => dispatch(updateConfig('display.uri.questions', !displayUriQuestions))
  const updateDisplayAttributesURI = () => dispatch(updateConfig('display.uri.attributes', !displayUriAttributes))
  const updateDisplayConditionsURI = () => dispatch(updateConfig('display.uri.conditions', !displayUriConditions))
  const updateDisplayOptionSetURI = () => dispatch(updateConfig('display.uri.optionsets', !displayUriOptionSets))

  const createQuestion = () => dispatch(createElement('questions'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Questions')}</strong>
          <BackButton />
          <NewButton onClick={createQuestion} />
        </div>
      </div>

      <div className="card-body">
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
        <div className="input-group input-group-sm">
          <label className="input-group-text">{gettext('Show URIs:')}</label>
          <button type="button" onClick={updateDisplayQuestionsURI} className={btnClass(displayUriQuestions)}>
            {gettext('Questions')}
          </button>
          <button type="button" onClick={updateDisplayAttributesURI} className={btnClass(displayUriAttributes)}>
            {gettext('Attributes')}
          </button>
          <button type="button" onClick={updateDisplayConditionsURI} className={btnClass(displayUriConditions)}>
            {gettext('Conditions')}
          </button>
          <button type="button" onClick={updateDisplayOptionSetURI} className={btnClass(displayUriOptionSets)}>
            {gettext('Option sets')}
          </button>
        </div>
      </div>
      {
        !isEmpty(questions) && (
          <ul className="list-group list-group-flush">
          {
            questions.map((question, index) => (
              <Question key={index} config={config} question={question}
                        filter="questions" filterEditors={true} />
            ))
          }
          </ul>
        )
      }
    </div>
  )
}

export default Questions
