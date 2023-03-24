import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Catalog from '../element/Catalog'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

const Catalogs = ({ config, catalogs, configActions, elementActions }) => {

  const updateFilterUri = (value) => configActions.updateConfig('filter.catalogs.uri', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.catalogs.uriPrefix', value)
  const updateDisplayURI = (value) => configActions.updateConfig('display.uri.catalogs', value)

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
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Catalogs')}</code>}
                    value={config.display.uri.catalogs} onChange={updateDisplayURI} />
        </div>
      </div>

      <ul className="list-group">
      {
        catalogs.map((catalog, index) => (
          <Catalog key={index} config={config} catalog={catalog}
                   elementActions={elementActions} filter={config.filter.catalogs} />
        ))
      }
      </ul>
    </div>
  )
}

Catalogs.propTypes = {
  config: PropTypes.object.isRequired,
  catalogs: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Catalogs
