import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements, getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Attribute from '../element/Attribute'
import { BackButton, NewButton } from '../common/ElementButtons'

const Attributes = ({ config, attributes, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.attributes.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.attributes.uriPrefix', uriPrefix)

  const createAttribute = () => elementActions.createElement('attributes')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createAttribute} />
        </div>
        <strong>{gettext('Attributes')}</strong>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterUri value={config.filter.attributes.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter attributes by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.attributes.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(attributes)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        filterElements(config.filter.attributes, attributes).map((attribute, index) => (
          <Attribute key={index} config={config} attribute={attribute}
                     elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Attributes.propTypes = {
  config: PropTypes.object.isRequired,
  attributes: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Attributes
