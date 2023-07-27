import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Section from '../element/Section'

const Sections = ({ config, sections, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.sections.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.sections.uri_prefix', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.editors', value)

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
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.sections.search', '')} onChange={updateFilterString}
                          placeholder={gettext('Filter sections')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.sections.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(sections)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                          options={config.sites} allLabel={gettext('All editors')} />
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
                   configActions={configActions} elementActions={elementActions}
                   filter="sections" filterEditors={true} />
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
