import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import Link from 'rdmo/core/assets/js/components/Link'

import { toggleDescendants } from '../../actions/elementActions'

import { getUriPrefixes } from '../../utils/filter'
import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton } from '../common/Buttons'
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

  const updateDisplayCatalogURI = (value) => dispatch(updateConfig('display.uri.catalogs', value))
  const updateDisplaySectionsURI = (value) => dispatch(updateConfig('display.uri.sections', value))
  const updateDisplayPagesURI = (value) => dispatch(updateConfig('display.uri.pages', value))
  const updateDisplayQuestionSetsURI = (value) => dispatch(updateConfig('display.uri.questionsets', value))
  const updateDisplayQuestionsURI = (value) => dispatch(updateConfig('display.uri.questions', value))
  const updateDisplayAttributesURI = (value) => dispatch(updateConfig('display.uri.attributes', value))
  const updateDisplayConditionsURI = (value) => dispatch(updateConfig('display.uri.conditions', value))
  const updateDisplayOptionSetURI = (value) => dispatch(updateConfig('display.uri.optionsets', value))

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Catalog catalog={catalog} display="plain" />
        </div>

        <div className="panel-body">
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
          <div className="mt-10">
            <span className="mr-10">{gettext('Toggle elements:')}</span>
            <Link className="mr-10" onClick={toggleSections}>{gettext('Sections')}</Link>
            <Link className="mr-10" onClick={togglePages}>{gettext('Pages')}</Link>
            <Link className="mr-10" onClick={toggleQuestionSets}>{gettext('Question sets')}</Link>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Catalogs')}</code>}
                      value={get(config, 'display.uri.catalogs', true)} onChange={updateDisplayCatalogURI} />
            <Checkbox label={<code className="code-questions">{gettext('Sections')}</code>}
                      value={get(config, 'display.uri.sections', true)} onChange={updateDisplaySectionsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Pages')}</code>}
                      value={get(config, 'display.uri.pages', true)} onChange={updateDisplayPagesURI} />
            <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                      value={get(config, 'display.uri.questionsets', true)} onChange={updateDisplayQuestionSetsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                      value={get(config, 'display.uri.questions', true)} onChange={updateDisplayQuestionsURI} />
            <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                      value={get(config, 'display.uri.attributes', true)} onChange={updateDisplayAttributesURI} />
            <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                      value={get(config, 'display.uri.conditions', true)} onChange={updateDisplayConditionsURI} />
            <Checkbox label={<code className="code-options">{gettext('Option sets')}</code>}
                      value={get(config, 'display.uri.optionsets', true)} onChange={updateDisplayOptionSetURI} />
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

    </>
  )
}

NestedCatalog.propTypes = {
  catalog: PropTypes.object.isRequired
}

export default NestedCatalog
