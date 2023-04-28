import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterUri, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Section from '../element/Section'

const Sections = ({ config, sections, configActions, elementActions }) => {

  const updateFilterUri = (value) => configActions.updateConfig('filter.sections.uri', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.sections.uriPrefix', value)
  const updateDisplayURI = (value) => configActions.updateConfig('display.uri.sections', value)

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
            <FilterUri value={config.filter.sections.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter sections by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.sections.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(sections)} />
          </div>
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Sections')}</code>}
                    value={config.display.uri.sections} onChange={updateDisplayURI} />
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
