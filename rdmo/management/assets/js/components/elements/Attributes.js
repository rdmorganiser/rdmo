import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterUri, FilterUriPrefix } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Attribute from '../element/Attribute'

const Attributes = ({ config, attributes, configActions, elementActions }) => {

  const updateFilterUri = (value) => configActions.updateConfig('filter.attributes.uri', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.attributes.uriPrefix', value)
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
        attributes.map((attribute, index) => (
          <Attribute key={index} config={config} attribute={attribute} elementActions={elementActions}
                     filter={config.filter.attributes} />
        ))
      }
      </ul>
    </div>
  )
}

Attributes.propTypes = {
  config: PropTypes.object.isRequired,
  attributes: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Attributes
