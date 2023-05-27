import React from 'react'
import PropTypes from 'prop-types'
import isEmpty from 'lodash/isEmpty'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton } from '../common/Buttons'
import { Drop } from '../common/DragAndDrop'

import Section from '../element/Section'
import Page from '../element/Page'

const NestedCatalog = ({ config, section, configActions, elementActions }) => {

  const updateFilterString = (uri) => configActions.updateConfig('filter.section.search', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.section.uri_prefix', uriPrefix)

  const updateDisplayPages = (value) => configActions.updateConfig('display.elements.pages', value)
  const updateDisplayQuestionSets = (value) => configActions.updateConfig('display.elements.questionsets', value)
  const updateDisplayQuestions = (value) => configActions.updateConfig('display.elements.questions', value)

  const updateDisplaySectionURI = (value) => configActions.updateConfig('display.uri.sections', value)
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
          <Section config={config} section={section}
                   elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={config.filter.section.search} onChange={updateFilterString}
                            placeholder={gettext('Filter sections')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.section.uri_prefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(section.elements)} />
            </div>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show elements:')}</span>
            <Checkbox label={gettext('Pages')} value={config.display.elements.pages} onChange={updateDisplayPages} />
            <Checkbox label={gettext('Question sets')} value={config.display.elements.questionsets} onChange={updateDisplayQuestionSets} />
            <Checkbox label={gettext('Questions')} value={config.display.elements.questions} onChange={updateDisplayQuestions} />
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Sections')}</code>}
                      value={config.display.uri.sections} onChange={updateDisplaySectionURI} />
            <Checkbox label={<code className="code-questions">{gettext('Pages')}</code>}
                      value={config.display.uri.pages} onChange={updateDisplayPagesURI} />
            <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                      value={config.display.uri.questionsets} onChange={updateDisplayQuestionSetsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                      value={config.display.uri.questions} onChange={updateDisplayQuestionsURI} />
            <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                      value={config.display.uri.attributes} onChange={updateDisplayAttributesURI} />
            <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                      value={config.display.uri.conditions} onChange={updateDisplayConditionsURI} />
            <Checkbox label={<code className="code-options">{gettext('Option sets')}</code>}
                      value={config.display.uri.optionsets} onChange={updateDisplayOptionSetURI} />
          </div>
        </div>
      </div>
      {
        !isEmpty(section.elements) &&
        <Drop element={section.elements[0]} elementActions={elementActions} indent={1} mode="before" />
      }
      {
        section.elements.map((page, index) => (
          <Page key={index} config={config} page={page} elementActions={elementActions}
                display="nested" filter={config.filter.section} indent={1} />
        ))
      }
    </>
  )
}

NestedCatalog.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedCatalog
