import React from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Section from '../element/Section'

const Sections = ({ config, sections, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.sections.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.sections.uri_prefix', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.sections.editors', value)
  const updateDisplaySectionURI = (value) => configActions.updateConfig('display.uri.sections', value)

  const createSection = () => elementActions.createElement('sections')

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
          <div className="col-sm-8">
            <FilterString value={config.filter.sections.search} onChange={updateFilterString}
                          placeholder={gettext('Filter sections')} />
          </div>
          <div className={config.settings.multisite ? 'col-sm-2' : 'col-sm-4'}>
            <FilterUriPrefix value={config.filter.sections.uri_prefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(sections)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={config.filter.sections.editors} onChange={updateFilterEditor}
                          options={config.sites} allLabel='All editors' />
            </div>
          }
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Sections')}</code>}
                    value={config.display.uri.sections} onChange={updateDisplaySectionURI} />
        </div>
      </div>

      <ul className="list-group">
      {
        sections.map((section, index) => (
          <Section key={index} config={config} section={section} elementActions={elementActions}
                   filter={config.filter.sections} />
        ))
      }
      </ul>
    </div>
  )
}

Sections.propTypes = {
  config: PropTypes.object.isRequired,
  sections: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Sections
