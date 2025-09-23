import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import get from 'lodash/get'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite} from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import View from '../element/View'

const Views = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const views = useSelector((state) => state.elements.views)

  const updateFilterString = (value) => dispatch(updateConfig('filter.views.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.views.uri_prefix', value))
  const updateFilterSite = (value) => dispatch(updateConfig('filter.sites', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const createView = () => dispatch(createElement('views'))

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createView} />
        </div>
        <strong>{gettext('Views')}</strong>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-4' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.views.search', '')} onChange={updateFilterString}
                          label={gettext('Filter views')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.views.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(views)} />
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
      </div>

      <ul className="list-group">
      {
        views.map((view, index) => (
          <View key={index} config={config} view={view}
                filter="views" filterSites={true} filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

export default Views
