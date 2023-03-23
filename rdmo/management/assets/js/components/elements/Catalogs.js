import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { filterElements, getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Catalog from '../element/Catalog'
import { BackButton, NewButton } from '../common/ElementButtons'

const Catalogs = ({ config, catalogs, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.catalogs.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.catalogs.uriPrefix', uriPrefix)

  const createCatalog = () => elementActions.createElement('catalogs')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createCatalog} />
        </div>
        <strong>{gettext('Catalogs')}</strong>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterUri value={config.filter.catalogs.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter catalogs by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.catalogs.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(catalogs)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        filterElements(config.filter.catalogs, catalogs).map((catalog, index) => (
          <Catalog key={index} config={config} catalog={catalog}
                   elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Catalogs.propTypes = {
  config: PropTypes.object.isRequired,
  catalogs: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Catalogs
