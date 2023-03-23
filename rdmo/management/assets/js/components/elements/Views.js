import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements, getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import View from '../element/View'
import { BackButton, NewButton } from '../common/ElementButtons'

const Views = ({ config, views, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.views.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.views.uriPrefix', uriPrefix)

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
        filterElements(config.filter.views, views).map((view, index) => (
          <View key={index} config={config} view={view}
                elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Views.propTypes = {
  config: PropTypes.object.isRequired,
  views: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Views
