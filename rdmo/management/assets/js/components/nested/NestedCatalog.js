import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'

import Link from 'rdmo/core/assets/js/components/Link'

import { getUriPrefixes } from '../../utils/filter'
import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton } from '../common/Buttons'
import { Drop } from '../common/DragAndDrop'

import Catalog from '../element/Catalog'
import Section from '../element/Section'

const NestedCatalog = ({ config, catalog, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.catalog.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.catalog.uri_prefix', value)

  const toggleSections = () => elementActions.toggleDescendants(catalog, 'sections')
  const togglePages = () => elementActions.toggleDescendants(catalog, 'pages')
  const toggleQuestionSets = () => elementActions.toggleDescendants(catalog, 'questionsets')

  const updateDisplayCatalogURI = (value) => configActions.updateConfig('display.uri.catalogs', value)
  const updateDisplaySectionsURI = (value) => configActions.updateConfig('display.uri.sections', value)
  const updateDisplayPagesURI = (value) => configActions.updateConfig('display.uri.pages', value)
  const updateDisplayQuestionSetsURI = (value) => configActions.updateConfig('display.uri.questionsets', value)
  const updateDisplayQuestionsURI = (value) => configActions.updateConfig('display.uri.questions', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)
  const updateDisplayConditionsURI = (value) => configActions.updateConfig('display.uri.conditions', value)
  const updateDisplayOptionSetURI = (value) => configActions.updateConfig('display.uri.optionsets', value)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Catalog config={config} catalog={catalog}
                   configActions={configActions} elementActions={elementActions} display="plain" />
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
        <Drop element={catalog.elements[0]} elementActions={elementActions} indent={0} mode="before" />
      }
      {
        catalog.elements.map((section, index) => {
          const sectionInfo = catalog.sections.find(info => info.section === section.id)
          const sectionOrder = sectionInfo ? sectionInfo.order : undefined

          return (
            <Section key={index}
              config={config}
              section={section}
              configActions={configActions}
              elementActions={elementActions}
              display="nested"
              filter="catalog"
              indent={0}
              order={sectionOrder}
            />
          )
        })
      }

    </>
  )
}

NestedCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedCatalog
