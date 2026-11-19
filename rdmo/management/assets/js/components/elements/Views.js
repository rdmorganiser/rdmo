import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import classNames from 'classnames'
import { isEmpty } from 'lodash'

import { useConfig, useConfigToggle } from 'rdmo/core/assets/js/hooks'

import { createElement } from '../../actions/elementActions'
import { getUriPrefixes } from '../../utils/filter'

import { BackButton, NewButton } from '../common/Buttons'
import { FilterSite, FilterString, FilterUriPrefix} from '../common/Filter'
import View from '../element/View'

const Views = () => {
  const dispatch = useDispatch()

  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const views = useSelector((state) => state.elements.views)

  const [filterString, setFilterString] = useConfig('filter.views.search', '')
  const [filterUriPrefix, setFilterUriPrefix] = useConfig('filter.views.uri_prefix', '')
  const [filterSite, setFilterSite] = useConfig('filter.sites', '')
  const [filterEditor, setFilterEditor] = useConfig('filter.editors', '')

  const [displayUriViews, toggleDisplayUriViews] = useConfigToggle('display.uri.views', true)


  const createView = () => dispatch(createElement('views'))

  const btnClass = (value) => classNames('btn border', value ? 'btn-light' : '')

  return (
    <div className="card card-tile">
      <div className="card-header">
        <div className="d-flex flex-column flex-sm-row align-items-sm-center gap-2">
          <strong className="flex-grow-1 text-center text-sm-start">{gettext('Views')}</strong>
          <BackButton />
          <NewButton onClick={createView} />
        </div>
      </div>

      <div className="card-body">
        <div className="mb-lg-2">
          <div className="row">
            <div className={settings.multisite ? 'col-sm-4' : 'col-sm-8'}>
              <FilterString
                value={filterString} onChange={setFilterString}
                label={gettext('Filter views')} />
            </div>
            <div className="col-sm-4">
              <FilterUriPrefix
                value={filterUriPrefix} onChange={setFilterUriPrefix}
                options={getUriPrefixes(views)} />
            </div>
            {
              settings.multisite && (
                <>
                  <div className="col-sm-2">
                    <FilterSite
                      value={filterSite} onChange={setFilterSite}
                      options={sites} />
                  </div>
                  <div className="col-sm-2">
                    <FilterSite
                      value={filterEditor} onChange={setFilterEditor}
                      options={sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
                  </div>
                </>
              )
            }
          </div>
        </div>
        <div className="input-group input-group-sm row-gap-1">
          <label className="input-group-text">{gettext('Show URIs')}</label>
          <button type="button" onClick={toggleDisplayUriViews} className={btnClass(displayUriViews)}>
            {gettext('Views')}
          </button>
        </div>
      </div>

      {
        !isEmpty(views) && (
          <ul className="list-group list-group-flush border-top">
            {
              views.map((view, index) => (
                <View
                  key={index} view={view}
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
