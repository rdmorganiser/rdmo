import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import View from '../element/View'
import ElementButtons from '../common/ElementButtons'

const Views = ({ config, views, fetchElement, storeElement }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons />
        <strong>{gettext('Views')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, views).map((view, index) => (
          <View key={index} config={config} view={view}
                fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Views.propTypes = {
  config: PropTypes.object.isRequired,
  views: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Views
