import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, AvailableLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Conditions = ({ config, conditions, fetchCondition, storeCondition }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchCondition(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Catalogs')} />
      <ul className="list-group">
      {
        filterElements(config, conditions).map((condition, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="element-options">
                <EditLink element={condition} verboseName={gettext('condition')}
                          onClick={condition => fetchCondition(condition.id)} />
                <LockedLink element={condition} verboseName={gettext('condition')}
                            onClick={locked => storeCondition(Object.assign({}, condition, { locked }))} />
                <ExportLink element={condition} verboseName={gettext('condition')} />
              </div>
              <div>
                <strong>{gettext('Condition')}{': '}</strong>
                <code className="code-conditions">{condition.uri}</code>
              </div>
            </li>
          )
        })
      }
      </ul>
    </div>
  )
}

Conditions.propTypes = {
  config: PropTypes.object.isRequired,
  conditions: PropTypes.array.isRequired,
  fetchCondition: PropTypes.func.isRequired,
  storeCondition: PropTypes.func.isRequired
}

export default Conditions
