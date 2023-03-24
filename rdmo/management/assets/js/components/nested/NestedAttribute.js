import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Attribute from '../element/Attribute'
import { BackButton } from '../common/ElementButtons'

const NestedAttribute = ({ config, attribute, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.attribute.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.attribute.uriPrefix', uriPrefix)

  return (
    <>
      <div className="panel panel-default panel-nested">
        <div className="panel-heading">
          <div className="pull-right">
            <BackButton />
          </div>
          <Attribute config={config} attribute={attribute}
                     elementActions={elementActions} display="plain" />
        </div>

        <div className="panel-body">
          <div className="row">
            <div className="col-sm-8">
              <FilterUri value={config.filter.attribute.uri} onChange={updateFilterUri}
                         placeholder={gettext('Filter attributes by URI')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix value={config.filter.attribute.uriPrefix} onChange={updateFilterUriPrefix}
                               options={getUriPrefixes(attribute.elements)} />
            </div>
          </div>
        </div>
      </div>

      {
        attribute.elements.map((attribute, index) => (
          <Attribute key={index} config={config} attribute={attribute} elementActions={elementActions}
                     display="nested" filter={config.filter.attribute} indent={1} />
        ))
      }
    </>
  )
}

NestedAttribute.propTypes = {
  config: PropTypes.object.isRequired,
  attribute: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default NestedAttribute
