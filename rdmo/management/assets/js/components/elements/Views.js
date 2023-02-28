import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Views = ({ config, views, fetchView }) => {
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
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit view')}
                   onClick={event => handleEdit(event, view.id)}>
                </a>
                {' '}
                <a href={view.xml_url} className="fa fa-download"
                   title={gettext('Export view as XML')}
                   target="blank">
                </a>
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
  fetchView: PropTypes.func.isRequired
}

export default Views
