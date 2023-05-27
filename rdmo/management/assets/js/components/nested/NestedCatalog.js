import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

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

  const updateDisplaySections = (value) => configActions.updateConfig('display.elements.sections', value)
  const updateDisplayPages = (value) => configActions.updateConfig('display.elements.pages', value)
  const updateDisplayQuestionSets = (value) => configActions.updateConfig('display.elements.questionsets', value)
  const updateDisplayQuestions = (value) => configActions.updateConfig('display.elements.questions', value)
  const updateDisplaySectionsURI = (value) => configActions.updateConfig('display.uri.sections', value)
  const updateDisplayPagesURI = (value) => configActions.updateConfig('display.uri.pages', value)
  const updateDisplayQuestionSetsURI = (value) => configActions.updateConfig('display.uri.questionsets', value)
  const updateDisplayQuestionsURI = (value) => configActions.updateConfig('display.uri.questions', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Catalog config={config} catalog={catalog}
                   elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={config.filter.catalog.search} onChange={updateFilterString}
                            placeholder={gettext('Filter catalogs')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.catalog.uri_prefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(catalog.elements)} />
            </div>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show elements:')}</span>
            <Checkbox label={gettext('Sections')} value={config.display.elements.sections} onChange={updateDisplaySections} />
            <Checkbox label={gettext('Pages')} value={config.display.elements.pages} onChange={updateDisplayPages} />
            <Checkbox label={gettext('Question sets')} value={config.display.elements.questionsets} onChange={updateDisplayQuestionSets} />
            <Checkbox label={gettext('Questions')} value={config.display.elements.questions} onChange={updateDisplayQuestions} />
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Sections')}</code>}
                      value={config.display.uri.sections} onChange={updateDisplaySectionsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Pages')}</code>}
                      value={config.display.uri.pages} onChange={updateDisplayPagesURI} />
            <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                      value={config.display.uri.questionsets} onChange={updateDisplayQuestionSetsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                      value={config.display.uri.questions} onChange={updateDisplayQuestionsURI} />
            <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                      value={config.display.uri.attributes} onChange={updateDisplayAttributesURI} />
          </div>
        </div>
      </div>
      {
        !isEmpty(catalog.elements) &&
        <Drop element={catalog.elements[0]} elementActions={elementActions} indent={0} mode="before" />
      }
      {
        catalog.elements.map((section, index) => (
          <Section key={index} config={config} section={section} elementActions={elementActions}
                   display="nested" filter={config.filter.catalog} indent={0} />
        ))
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
