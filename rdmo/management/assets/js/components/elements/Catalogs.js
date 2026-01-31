import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite} from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import Catalog from '../element/Catalog'

const Catalogs = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const catalogs = useSelector((state) => state.elements.catalogs)

  const updateFilterString = (value) => dispatch(updateConfig('filter.catalogs.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.catalogs.uri_prefix', value))
  const updateFilterSite = (value) => dispatch(updateConfig('filter.sites', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const displayUriCatalogs = isTruthy(get(config, 'display.uri.catalogs', true))

  const toggleDisplayUriCatalogs = () => dispatch(updateConfig('display.uri.catalogs', !displayUriCatalogs))

  const createCatalog = () => dispatch(createElement('catalogs'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Catalogs')}</strong>
          <BackButton />
          <NewButton onClick={createCatalog} />
        </div>
      </div>

      <div className="card-body">
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
        <div className="input-group input-group-sm">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={toggleDisplayUriCatalogs} className={btnClass(displayUriCatalogs)}>
            {gettext('Catalogs')}
          </button>
        </div>
      </div>

      {
        !isEmpty(catalogs) && (
          <ul className="list-group list-group-flush">
          {
            catalogs.map((catalog, index) => (
              <Catalog key={index} config={config} catalog={catalog}
                       filter="catalogs" filterSites={true} filterEditors={true} />
            ))
          }
          </ul>
        )
      }
    </div>
  )
}

export default Catalogs
