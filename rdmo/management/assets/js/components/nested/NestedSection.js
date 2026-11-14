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
import Section from '../element/Section'

const NestedSection = ({ section }) => {
  const dispatch = useDispatch()

  const [filterString, setFilterString] = useConfig('filter.section.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.section.uri_prefix', '')

  const togglePages = () => dispatch(toggleDescendants(section, 'pages'))
  const toggleQuestionSets = () => dispatch(toggleDescendants(section, 'questionsets'))

  const [displayUriSections, toggleDisplayUriSections] = useConfigToggle('display.uri.sections', true)
  const [displayUriPages, toggleDisplayUriPages] = useConfigToggle('display.uri.pages', true)
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
          <Section section={section} display="plain" backButton={true} />
        </div>

        <div className="card-body">
          <div className="mb-lg-2">
            <div className="row">
              <div className="col-sm-8">
                <FilterString
                  value={filterString} onChange={setFilterString}
                  label={gettext('Filter sections')} />
              </div>
              <div className="col-sm-4">
                <FilterUriPrefix
                  value={filterUriPrefix} onChange={setFilterUriPrefix}
                  options={getUriPrefixes(section.elements)} />
              </div>
            </div>
          </div>
          <div className="input-group input-group-sm row-gap-1 mb-2">
            <label className="input-group-text">{gettext('Show URIs')}</label>
            <button type="button" onClick={toggleDisplayUriSections} className={btnClass(displayUriSections)}>
              {gettext('Sections')}
            </button>
            <button type="button" onClick={toggleDisplayUriPages} className={btnClass(displayUriPages)}>
              {gettext('Pages')}
            </button>
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
            <button type="button" onClick={togglePages} className="btn btn-outline-primary border">
              {gettext('Pages')}
            </button>
            <button type="button" onClick={toggleQuestionSets} className="btn btn-outline-primary border">
              {gettext('Question sets')}
            </button>
          </div>
        </div>

        <div className="card-body border-top pt-0">
          {
            !isEmpty(section.elements) &&
            <Drop element={section.elements[0]} indent={1} mode="before" />
          }
          {
            section.elements.map((page, index) => (
              <Page
                key={index} page={page}
                display="nested" filter="section" indent={1} />
            ))
          }
        </div>
      </div>
    </>
  )
}

NestedSection.propTypes = {
  section: PropTypes.object.isRequired
}

export default NestedSection
