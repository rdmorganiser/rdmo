import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, AvailableLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Views = ({ config, views, fetchView, storeView }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchView(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Views')} />

      <ul className="list-group">
      {
        filterElements(config, views).map((view, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="element-options">
                <EditLink element={view} verboseName={gettext('view')}
                          onClick={view => fetchView(view.id)} />
                <AvailableLink element={view} verboseName={gettext('view')}
                               onClick={available => storeView(Object.assign({}, view, { available }))} />
                <LockedLink element={view} verboseName={gettext('view')}
                            onClick={locked => storeView(Object.assign({}, view, { locked }))} />
                <ExportLink element={view} verboseName={gettext('view')} />
              </div>
              <div>
                <strong>{gettext('View')}{': '}</strong>
                <code className="code-views">{view.uri}</code>
              </div>
            </li>
          )
        })
      }
      </ul>
    </div>
  )
}

Views.propTypes = {
  config: PropTypes.object.isRequired,
  views: PropTypes.array.isRequired,
  fetchView: PropTypes.func.isRequired,
  storeView: PropTypes.func.isRequired
}

export default Views
