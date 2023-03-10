import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Attributes = ({ config, attributes, fetchAttribute, storeAttribute }) => {
  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Attributes')} />
      <ul className="list-group">
      {
        filterElements(config, attributes).map((attribute, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="element-options">
                <EditLink element={attribute} verboseName={gettext('attribute')}
                          onClick={attribute => fetchAttribute(attribute.id)} />
                <LockedLink element={attribute} verboseName={gettext('attribute')}
                            onClick={locked => storeAttribute(Object.assign({}, attribute, { locked }))} />
                <ExportLink element={attribute} verboseName={gettext('attribute')} />
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
  fetchAttribute: PropTypes.func.isRequired,
  storeAttribute: PropTypes.func.isRequired
}

export default Attributes
