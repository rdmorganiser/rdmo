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

import Section from '../element/Section'
import Page from '../element/Page'

const NestedSection = ({ section }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const updateFilterString = (uri) => dispatch(updateConfig('filter.section.search', uri))
  const updateFilterUriPrefix = (uriPrefix) => dispatch(updateConfig('filter.section.uri_prefix', uriPrefix))

  const togglePages = () => dispatch(toggleDescendants(section, 'pages'))
  const toggleQuestionSets = () => dispatch(toggleDescendants(section, 'questionsets'))

  const updateDisplaySectionURI = (value) => dispatch(updateConfig('display.uri.sections', value))
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
          <Section section={section} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterString value={get(config, 'filter.section.search', '')} onChange={updateFilterString}
                            label={gettext('Filter sections')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={get(config, 'filter.section.uri_prefix', '')} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(section.elements)} />
            </div>
          </div>
          <div className="mt-10">
            <span className="mr-10">{gettext('Show elements:')}</span>
            <Link className="mr-10" onClick={togglePages}>{gettext('Pages')}</Link>
            <Link className="mr-10" onClick={toggleQuestionSets}>{gettext('Question sets')}</Link>
          </div>
          <div className="checkboxes">
            <span className="mr-10">{gettext('Show URIs:')}</span>
            <Checkbox label={<code className="code-questions">{gettext('Sections')}</code>}
                      value={get(config, 'config.display.uri.sections', true)} onChange={updateDisplaySectionURI} />
            <Checkbox label={<code className="code-questions">{gettext('Pages')}</code>}
                      value={get(config, 'config.display.uri.pages', true)} onChange={updateDisplayPagesURI} />
            <Checkbox label={<code className="code-questions">{gettext('Question sets')}</code>}
                      value={get(config, 'config.display.uri.questionsets', true)} onChange={updateDisplayQuestionSetsURI} />
            <Checkbox label={<code className="code-questions">{gettext('Questions')}</code>}
                      value={get(config, 'config.display.uri.questions', true)} onChange={updateDisplayQuestionsURI} />
            <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                      value={get(config, 'config.display.uri.attributes', true)} onChange={updateDisplayAttributesURI} />
            <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                      value={get(config, 'config.display.uri.conditions', true)} onChange={updateDisplayConditionsURI} />
            <Checkbox label={<code className="code-options">{gettext('Option sets')}</code>}
                      value={get(config, 'config.display.uri.optionsets', true)} onChange={updateDisplayOptionSetURI} />
          </div>
        </div>
      </div>
      {
        !isEmpty(section.elements) &&
        <Drop element={section.elements[0]} indent={1} mode="before" />
      }
      {
        section.elements.map((page, index) => (
          <Page key={index} config={config} page={page}
                display="nested" filter="section" indent={1} />
        ))
      }
    </>
  )
}

NestedSection.propTypes = {
  section: PropTypes.object.isRequired
}

export default NestedSection
