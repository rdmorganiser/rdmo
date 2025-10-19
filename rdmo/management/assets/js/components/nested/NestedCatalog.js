import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { toggleDescendants } from '../../actions/elementActions'

import { getUriPrefixes } from '../../utils/filter'
import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Drop } from '../common/DragAndDrop'

import Catalog from '../element/Catalog'
import Section from '../element/Section'

const NestedCatalog = ({ catalog }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const updateFilterString = (value) => dispatch(updateConfig('filter.catalog.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.catalog.uri_prefix', value))

  const toggleSections = () => dispatch(toggleDescendants(catalog, 'sections'))
  const togglePages = () => dispatch(toggleDescendants(catalog, 'pages'))
  const toggleQuestionSets = () => dispatch(toggleDescendants(catalog, 'questionsets'))

  const displayUriCatalogs = isTruthy(get(config, 'display.uri.catalogs', true))
  const displayUriSections = isTruthy(get(config, 'display.uri.sections', true))
  const displayUriPages = isTruthy(get(config, 'display.uri.pages', true))
  const displayUriQuestionSets = isTruthy(get(config, 'display.uri.questionsets', true))
  const displayUriQuestions = isTruthy(get(config, 'display.uri.questions', true))
  const displayUriAttributes = isTruthy(get(config, 'display.uri.attributes', true))
  const displayUriConditions = isTruthy(get(config, 'display.uri.conditions', true))
  const displayUriOptionSets = isTruthy(get(config, 'display.uri.optionsets', true))

  const toggleDisplayUriCatalogs = () => dispatch(updateConfig('display.uri.catalogs', !displayUriCatalogs))
  const toggleDisplayUriSections = () => dispatch(updateConfig('display.uri.sections', !displayUriSections))
  const toggleDisplayUriPages = () => dispatch(updateConfig('display.uri.pages', !displayUriPages))
  const toggleDisplayUriQuestionSets = () => dispatch(updateConfig('display.uri.questionsets', !displayUriQuestionSets))
  const toggleDisplayUriQuestions = () => dispatch(updateConfig('display.uri.questions', !displayUriQuestions))
  const toggleDisplayUriAttributes = () => dispatch(updateConfig('display.uri.attributes', !displayUriAttributes))
  const toggleDisplayUriConditions = () => dispatch(updateConfig('display.uri.conditions', !displayUriConditions))
  const toggleDisplayUriOptionSets = () => dispatch(updateConfig('display.uri.optionsets', !displayUriOptionSets))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="position-relative">
      <div className="card">
        <div className="card-header">
          <Catalog catalog={catalog} display="plain" backButton={true} />
        </div>

        <div className="card-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={get(config, 'filter.catalog.search', '')} onChange={updateFilterString}
                            label={gettext('Filter catalogs')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={get(config, 'filter.catalog.uri_prefix', '')} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(catalog.elements)} />
            </div>
          </div>
          <div className="input-group input-group-sm mb-2">
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
          <div className="input-group input-group-sm">
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
      </div>
      {
        !isEmpty(catalog.elements) &&
        <Drop element={catalog.elements[0]} indent={0} mode="before" />
      }
      {
        catalog.elements.map((section, index) => {
          const sectionInfo = catalog.sections.find(info => info.section === section.id)
          const sectionOrder = sectionInfo ? sectionInfo.order : undefined

          return (
            <Section key={index} section={section} display="nested" filter="catalog" indent={0} order={sectionOrder} />
          )
        })
      }

    </div>
  )
}

NestedCatalog.propTypes = {
  catalog: PropTypes.object.isRequired
}

export default NestedCatalog
