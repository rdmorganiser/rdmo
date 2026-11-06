import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { useConfig } from 'rdmo/core/assets/js/hooks'

import { toggleDescendants } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { Drop } from '../common/DragAndDrop'
import { FilterString, FilterUriPrefix } from '../common/Filter'
import Catalog from '../element/Catalog'
import Section from '../element/Section'

const NestedCatalog = ({ catalog }) => {
  const dispatch = useDispatch()

  const [filterString, setFilterString] = useConfig('filter.catalog.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.catalog.uri_prefix', '')

  const toggleSections = () => dispatch(toggleDescendants(catalog, 'sections'))
  const togglePages = () => dispatch(toggleDescendants(catalog, 'pages'))
  const toggleQuestionSets = () => dispatch(toggleDescendants(catalog, 'questionsets'))

  const [displayUriCatalogs, setDisplayUriCatalogs] = useConfig('display.uri.catalogs', true)
  const [displayUriSections, setDisplayUriSections] = useConfig('display.uri.sections', true)
  const [displayUriPages, setDisplayUriPages] = useConfig('display.uri.pages', true)
  const [displayUriQuestionSets, setDisplayUriQuestionSets] = useConfig('display.uri.questionsets', true)
  const [displayUriQuestions, setDisplayUriQuestions] = useConfig('display.uri.questions', true)
  const [displayUriAttributes, setDisplayUriAttributes] = useConfig('display.uri.attributes', true)
  const [displayUriConditions, setDisplayUriConditions] = useConfig('display.uri.conditions', true)
  const [displayUriOptionSets, setDisplayUriOptionSets] = useConfig('display.uri.optionsets', true)

  const toggleDisplayUriCatalogs = () => setDisplayUriCatalogs(!displayUriCatalogs)
  const toggleDisplayUriSections = () => setDisplayUriSections(!displayUriSections)
  const toggleDisplayUriPages = () => setDisplayUriPages(!displayUriPages)
  const toggleDisplayUriQuestionSets = () => setDisplayUriQuestionSets(!displayUriQuestionSets)
  const toggleDisplayUriQuestions = () => setDisplayUriQuestions(!displayUriQuestions)
  const toggleDisplayUriAttributes = () => setDisplayUriAttributes(!displayUriAttributes)
  const toggleDisplayUriConditions = () => setDisplayUriConditions(!displayUriConditions)
  const toggleDisplayUriOptionSets = () => setDisplayUriOptionSets(!displayUriOptionSets)

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="position-relative">
      <div className="card card-tile">
        <div className="card-header">
          <Catalog catalog={catalog} display="plain" backButton={true} />
        </div>

        <div className="card-body">
          <div className="mb-lg-2">
            <div className="row">
              <div className="col-sm-8">
                <FilterString
                  value={filterString} onChange={setFilterString}
                  label={gettext('Filter catalogs')} />
              </div>
              <div className="col-sm-4">
                <FilterUriPrefix
                  value={filterUriPrefix} onChange={setFilterUriPrefix}
                  options={getUriPrefixes(catalog.elements)} />
              </div>
            </div>
          </div>
          <div className="input-group input-group-sm row-gap-1 mb-2">
            <label className="input-group-text">{gettext('Show URIs')}</label>
            <button type="button" onClick={toggleDisplayUriCatalogs} className={btnClass(displayUriCatalogs)}>
              {gettext('Catalogs')}
            </button>
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
            <button type="button" onClick={toggleSections} className="btn btn-outline-primary border">
              {gettext('Sections')}
            </button>
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
            !isEmpty(catalog.elements) &&
            <Drop element={catalog.elements[0]} indent={0} mode="before" />
          }
          {
            catalog.elements.map((section, index) => {
              const sectionInfo = catalog.sections.find(info => info.section === section.id)
              const sectionOrder = sectionInfo ? sectionInfo.order : undefined

              return (
                <Section
                  key={index}
                  section={section}
                  display="nested"
                  filter="catalog"
                  indent={0}
                  order={sectionOrder}
                />
              )
            })
          }
        </div>
      </div>
    </div>
  )
}

NestedCatalog.propTypes = {
  catalog: PropTypes.object.isRequired
}

export default NestedCatalog
