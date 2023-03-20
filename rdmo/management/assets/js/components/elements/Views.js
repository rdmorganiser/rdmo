import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import View from '../element/View'
import { BackButton, NewButton } from '../common/ElementButtons'

const Views = ({ config, views, elementActions }) => {

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

      <ul className="list-group">
      {
        filterElements(config, views).map((view, index) => (
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
