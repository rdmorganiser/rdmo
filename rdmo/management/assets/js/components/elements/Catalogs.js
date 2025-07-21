import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite} from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Catalog from '../element/Catalog'

const Catalogs = ({ config, catalogs, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.catalogs.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.catalogs.uri_prefix', value)
  const updateFilterSite = (value) => configActions.updateConfig('filter.sites', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.editors', value)
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
            <FilterString value={get(config, 'filter.catalogs.search', '')} onChange={updateFilterString}
                          label={gettext('Filter catalogs')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.catalogs.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(catalogs)} />
          </div>
          {
            config.settings.multisite && <>
              <div className="col-sm-2">
                <FilterSite value={get(config, 'filter.sites', '')} onChange={updateFilterSite}
                            options={config.sites} />
              </div>
              <div className="col-sm-2">
                <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                            options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
              </div>
            </>
          }
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Catalogs')}</code>}
                    value={get(config, 'display.uri.catalogs', true)} onChange={updateDisplayCatalogURI} />
        </div>
      </div>

      <ul className="list-group">
      {
        catalogs.map((catalog, index) => (
          <Catalog key={index} config={config} catalog={catalog}
                   configActions={configActions} elementActions={elementActions}
                   filter="catalogs" filterSites={true} filterEditors={true} />
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
