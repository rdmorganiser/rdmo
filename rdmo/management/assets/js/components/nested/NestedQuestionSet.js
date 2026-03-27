import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { toggleDescendants } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { Drop } from '../common/DragAndDrop'
import { FilterString, FilterUriPrefix } from '../common/Filter'
import Question from '../element/Question'
import QuestionSet from '../element/QuestionSet'

const NestedQuestionSet = ({ questionset }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const updateFilterString = (uri) => dispatch(updateConfig('filter.questionset.search', uri))
  const updateFilterUriPrefix = (uriPrefix) => dispatch(updateConfig('filter.questionset.uri_prefix', uriPrefix))

  const toggleQuestionSets = () => dispatch(toggleDescendants(questionset, 'questionsets'))

  const displayUriQuestionSets = isTruthy(get(config, 'display.uri.questionsets', true))
  const displayUriQuestions = isTruthy(get(config, 'display.uri.questions', true))
  const displayUriAttributes = isTruthy(get(config, 'display.uri.attributes', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))
  const displayUriOptionSets = isTruthy(get(config, 'display.uri.optionsets', true))

  const toggleDisplayUriQuestionSets = () => dispatch(updateConfig('display.uri.questionsets', !displayUriQuestionSets))
  const toggleDisplayUriQuestions = () => dispatch(updateConfig('display.uri.questions', !displayUriQuestions))
  const toggleDisplayUriAttributes = () => dispatch(updateConfig('display.uri.attributes', !displayUriAttributes))
  const toggleDisplayUriConditions = () => dispatch(updateConfig('display.uri.conditions', !displayUriConditions))
  const toggleDisplayUriOptionSets = () => dispatch(updateConfig('display.uri.optionsets', !displayUriOptionSets))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <>
      <div className="card">
        <div className="card-header">
          <QuestionSet questionset={questionset} display="plain" backButton={true} />
        </div>

        <div className="card-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={get(config, 'filter.questionset.search', '')} onChange={updateFilterString}
                label={gettext('Filter question sets')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={get(config, 'filter.questionset.uri_prefix', '')} onChange={updateFilterUriPrefix}
                options={getUriPrefixes(questionset.elements)} />
            </div>
          </div>
          <div className="input-group input-group-sm mb-2">
            <label className="input-group-text">{gettext('Show URIs')}</label>
            <button type="button" onClick={toggleDisplayUriQuestionSets} className={btnClass(displayUriQuestionSets)}>
              {gettext('Question sets')}
            </button>
            <button type="button" onClick={toggleDisplayUriQuestions} className={btnClass(displayUriQuestions)}>
              {gettext('Questions')}
            </button>
            <button type="button" onClick={toggleDisplayUriAttributes} className={btnClass(displayUriAttributes)}>
              {gettext('Attributes')}
            </button>
            <button type="button" onClick={toggleDisplayUriConditions} className={btnClass(displayUriConditions)}>
              {gettext('Conditions')}
            </button>
            <button type="button" onClick={toggleDisplayUriOptionSets} className={btnClass(displayUriOptionSets)}>
              {gettext('Option sets')}
            </button>
          </div>
          <div className="input-group input-group-sm">
            <label className="input-group-text">{gettext('Toggle elements')}</label>
            <button type="button" onClick={toggleQuestionSets} className="btn btn-outline-primary border">
              {gettext('Question sets')}
            </button>
          </div>
        </div>
      </div>
      {
        !isEmpty(questionset.elements) &&
        <Drop element={questionset.elements[0]} indent={1} mode="before" />
      }
      {
        questionset.elements.map((element, index) => {
          if (element.model == 'questions.questionset') {
            return <QuestionSet key={index} questionset={element} display="nested" filter="questionset" indent={1} />
          } else {
            return <Question key={index} question={element} display="nested" filter="questionset" indent={1} />
          }
        })
      }
    </>
  )
}

NestedQuestionSet.propTypes = {
  questionset: PropTypes.object.isRequired,
}

export default NestedQuestionSet
