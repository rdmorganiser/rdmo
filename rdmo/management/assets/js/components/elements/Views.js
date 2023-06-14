import React from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import View from '../element/View'

const Views = ({ config, views, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.views.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.views.uri_prefix', value)
  const updateFilterSite = (value) => configActions.updateConfig('filter.views.sites', value)

  const createView = () => elementActions.createElement('views')

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
            <FilterString value={config.filter.views.search} onChange={updateFilterString}
                          placeholder={gettext('Filter views')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.views.uri_prefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(views)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-4">
              <FilterSite value={config.filter.views.sites} onChange={updateFilterSite}
                          options={config.sites} />
            </div>
          }
        </div>
      </div>

      <ul className="list-group">
      {
        views.map((view, index) => (
          <View key={index} config={config} view={view} elementActions={elementActions}
                filter={config.filter.views} />
        ))
      }
      </ul>
    </div>
  )
}

Views.propTypes = {
  config: PropTypes.object.isRequired,
  views: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Views
