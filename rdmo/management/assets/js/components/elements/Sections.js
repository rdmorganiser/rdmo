import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Section from '../element/Section'

const Sections = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const sections = useSelector((state) => state.elements.sections)

  const updateFilterString = (value) => dispatch(updateConfig('filter.sections.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.sections.uri_prefix', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const updateDisplaySectionURI = (value) => dispatch(updateConfig('display.uri.sections', value))

  const createSection = () => dispatch(createElement('sections'))

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createSection} />
        </div>
        <strong>{gettext('Sections')}</strong>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.sections.search', '')} onChange={updateFilterString}
                          label={gettext('Filter sections')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.sections.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(sections)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                          options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
            </div>
          }
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Sections')}</code>}
                    value={get(config, 'display.uri.sections', true)} onChange={updateDisplaySectionURI} />
        </div>
      </div>

      <ul className="list-group">
      {
        sections.map((section, index) => (
          <Section key={index} config={config} section={section}
                   filter="sections" filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

export default Sections
