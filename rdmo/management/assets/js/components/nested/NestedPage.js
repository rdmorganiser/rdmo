import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { useConfig, useConfigToggle } from 'rdmo/core/assets/js/hooks'

import { toggleDescendants } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { Drop } from '../common/DragAndDrop'
import { FilterString, FilterUriPrefix } from '../common/Filter'
import Page from '../element/Page'
import Question from '../element/Question'
import QuestionSet from '../element/QuestionSet'

const NestedPage = ({ page }) => {
  const dispatch = useDispatch()

  const [filterString, setFilterString] = useConfig('filter.page.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.page.uri_prefix', '')

  const toggleQuestionSets = () => dispatch(toggleDescendants(page, 'questionsets'))

  const [displayUriQuestionSets, toggleDisplayUriQuestionSets] = useConfigToggle('display.uri.questionsets', true)
  const [displayUriQuestions, toggleDisplayUriQuestions] = useConfigToggle('display.uri.questions', true)
  const [displayUriAttributes, toggleDisplayUriAttributes] = useConfigToggle('display.uri.attributes', true)
  const [displayUriConditions, toggleDisplayUriConditions] = useConfigToggle('display.uri.conditions', true)
  const [displayUriOptionSets, toggleDisplayUriOptionSets] = useConfigToggle('display.uri.optionsets', true)


  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <>
      <div className="card">
        <div className="card-header">
          <Page page={page} display="plain" backButton={true} />
        </div>

        <div className="card-body">
          <div className="mb-lg-2">
            <div className="row">
              <div className="col-sm-8">
                <FilterString
                  value={filterString} onChange={setFilterString}
                  label={gettext('Filter pages')} />
              </div>
              <div className="col-sm-4">
                <FilterUriPrefix
                  value={filterUriPrefix} onChange={setFilterUriPrefix}
                  options={getUriPrefixes(page.elements)} />
              </div>
            </div>
          </div>
          <div className="input-group input-group-sm row-gap-1 mb-2">
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
          <div className="input-group input-group-sm row-gap-1">
            <label className="input-group-text">{gettext('Toggle elements')}</label>
            <button type="button" onClick={toggleQuestionSets} className="btn btn-outline-primary border">
              {gettext('Question sets')}
            </button>
          </div>
        </div>

        <div className="card-body border-top pt-0">
          {
            !isEmpty(page.elements) &&
            <Drop element={page.elements[0]} indent={1} mode="before" />
          }
          {
            page.elements.map((element, index) => {
              if (element.model == 'questions.questionset') {
                return <QuestionSet key={index} questionset={element} display="nested" filter="page" indent={1} />
              } else {
                return <Question key={index} question={element} display="nested" filter="page" indent={1} />
              }
            })
          }
        </div>
      </div>
    </>
  )
}

NestedPage.propTypes = {
  page: PropTypes.object.isRequired
}

export default NestedPage
