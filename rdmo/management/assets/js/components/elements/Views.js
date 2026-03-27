import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { get, isEmpty } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix} from '../common/Filter'
import View from '../element/View'

const Views = () => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const views = useSelector((state) => state.elements.views)

  const updateFilterString = (value) => dispatch(updateConfig('filter.views.search', value))
  const updateFilterUriPrefix = (value) => dispatch(updateConfig('filter.views.uri_prefix', value))
  const updateFilterSite = (value) => dispatch(updateConfig('filter.sites', value))
  const updateFilterEditor = (value) => dispatch(updateConfig('filter.editors', value))

  const displayUriViews = isTruthy(get(config, 'display.uri.views', true))

  const updateDisplayUriViews = () => dispatch(updateConfig('display.uri.views', !displayUriViews))

  const createView = () => dispatch(createElement('views'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex align-items-center gap-2">
          <strong className="me-auto">{gettext('Views')}</strong>
          <BackButton />
          <NewButton onClick={createView} />
        </div>
      </div>

      <div className="card-body">
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
            config.settings.multisite && (
              <>
                <div className="col-sm-2">
                  <FilterSite value={get(config, 'filter.sites', '')} onChange={updateFilterSite}
                    options={config.sites} />
                </div>
                <div className="col-sm-2">
                  <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                    options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
                </div>
              </>
            )
          }
        </div>
        <div className="input-group input-group-sm">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={updateDisplayUriViews} className={btnClass(displayUriViews)}>
            {gettext('Views')}
          </button>
        </div>
      </div>

      {
        !isEmpty(views) && (
          <ul className="list-group list-group-flush">
            {
              views.map((view, index) => (
                <View key={index} config={config} view={view}
                  filter="views" filterSites={true} filterEditors={true} />
              ))
            }
          </ul>
        )
      }
    </div>
  )
}

export default Views
