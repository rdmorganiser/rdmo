import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { useConfig, useConfigToggle } from 'rdmo/core/assets/js/hooks'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix } from '../common/Filter'
import Question from '../element/Question'

const Questions = () => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const questions = useSelector((state) => state.elements.questions)

  const [filterString, setFilterString] = useConfig('filter.questions.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.questions.uri_prefix', '')
  const [filterEditor, setFilterEditor] = useConfig('filter.editors', '')

  const [displayUriQuestions, toggleDisplayUriQuestions] = useConfigToggle('display.uri.questions', true)
  const [displayUriAttributes, toggleDisplayUriAttributes] = useConfigToggle('display.uri.attributes', true)
  const [displayUriConditions, toggleDisplayUriConditions] = useConfigToggle('display.uri.conditions', true)
  const [displayUriOptionSets, toggleDisplayUriOptionSets] = useConfigToggle('display.uri.optionsets', true)


  const createQuestion = () => dispatch(createElement('questions'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2">
          <strong className="flex-grow-1 text-center text-sm-start">{gettext('Questions')}</strong>
          <BackButton />
          <NewButton onClick={createQuestion} />
        </div>
      </div>

      <div className="card-body">
        <div className="mb-lg-2">
          <div className="row">
            <div className={settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
              <FilterString
                value={filterString} onChange={setFilterString}
                label={gettext('Filter questions')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix
                value={filterUriPrefix} onChange={setFilterUriPrefix}
                options={getUriPrefixes(questions)} />
            </div>
            {
              settings.multisite && (
                <div className="col-sm-2">
                  <FilterSite
                    value={filterEditor} onChange={setFilterEditor}
                    options={sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
                </div>
              )
            }
          </div>
        </div>
        <div className="input-group input-group-sm row-gap-1">
          <label className="input-group-text">{gettext('Show URIs:')}</label>
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
      </div>
      {
        !isEmpty(questions) && (
          <ul className="list-group list-group-flush border-top">
            {
              questions.map((question, index) => (
                <Question
                  key={index} question={question}
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
