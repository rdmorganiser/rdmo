import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Section from '../element/Section'
import Page from '../element/Page'
import { BackButton } from '../common/ElementButtons'

const NestedCatalog = ({ config, section, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.section.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.section.uriPrefix', uriPrefix)

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
              <FilterUri value={config.filter.section.uri} onChange={updateFilterUri}
                         placeholder={gettext('Filter sections by URI')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.section.uriPrefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(section.elements)} />
            </div>
          </div>
        </div>
      </div>

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
