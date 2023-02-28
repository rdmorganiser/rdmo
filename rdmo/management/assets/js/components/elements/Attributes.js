import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Attributes = ({ config, attributes, fetchAttribute }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchAttribute(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Attributes')} />
      <ul className="list-group">
      {
        filterElements(config, attributes).map((attribute, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit attribute')}
                   onClick={event => handleEdit(event, attribute.id)}>
                </a>
                {' '}
                <a href={attribute.xml_url} className="fa fa-download"
                   title={gettext('Export attribute as XML')}
                   target="blank">
                </a>
              </div>
              <div>
                <strong>{gettext('Attribute')}{': '}</strong>
                <code className="code-domain">{attribute.uri}</code>
              </div>
            </li>
          )
        })
      }
      </ul>
    </div>
  )
}

Attributes.propTypes = {
  config: PropTypes.object.isRequired,
  attributes: PropTypes.array.isRequired,
  fetchAttribute: PropTypes.func.isRequired
}

export default Attributes
