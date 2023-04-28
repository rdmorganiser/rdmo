import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterUri, FilterUriPrefix } from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'

import View from '../element/View'

const Views = ({ config, views, configActions, elementActions }) => {

  const updateFilterUri = (value) => configActions.updateConfig('filter.views.uri', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.views.uriPrefix', value)

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
          <div className="col-sm-8">
            <FilterUri value={config.filter.views.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter views by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.views.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(views)} />
          </div>
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
