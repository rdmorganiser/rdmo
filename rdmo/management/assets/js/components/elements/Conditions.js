import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Conditions = ({ config, conditions, fetchCondition }) => {
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
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit section')}
                   onClick={event => handleEdit(event, condition.id)}>
                </a>
                {' '}
                <a href={condition.xml_url} className="fa fa-download"
                   title={gettext('Export condition as XML')}
                   target="blank">
                </a>
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
  fetchCondition: PropTypes.func.isRequired
}

export default Conditions
