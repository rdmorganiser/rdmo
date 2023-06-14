import React from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Catalog from '../element/Catalog'

const Catalogs = ({ config, catalogs, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.catalogs.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.catalogs.uri_prefix', value)
  const updateFilterSite = (value) => configActions.updateConfig('filter.catalogs.sites', value)
  const updateDisplayCatalogURI = (value) => configActions.updateConfig('display.uri.catalogs', value)

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
          <div className={config.settings.multisite ? 'col-sm-4' : 'col-sm-8'}>
            <FilterString value={config.filter.catalogs.search} onChange={updateFilterString}
                          placeholder={gettext('Filter catalogs')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.catalogs.uri_prefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(catalogs)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-4">
              <FilterSite value={config.filter.catalogs.sites} onChange={updateFilterSite}
                          options={config.sites} />
            </div>
          }
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Catalogs')}</code>}
                    value={config.display.uri.catalogs} onChange={updateDisplayCatalogURI} />
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
