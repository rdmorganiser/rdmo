import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const OptionSets = ({ config, optionsets, fetchOptionSet }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchOptionSet(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Catalogs')} />
      <ul className="list-group">
      {
        filterElements(config, optionsets).map((optionset, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit optionset')}
                   onClick={event => handleEdit(event, optionset.id)}>
                </a>
                {' '}
                <a href={optionset.xml_url} className="fa fa-download"
                   title={gettext('Export optionset as XML')}
                   target="blank">
                </a>
              </div>
              <div>
                <strong>{gettext('Option set')}{': '}</strong>
                <code className="code-options">{optionset.uri}</code>
              </div>
            </li>
          )
        })
      }
      </ul>
    </div>
  )
}

OptionSets.propTypes = {
  config: PropTypes.object.isRequired,
  optionsets: PropTypes.array.isRequired,
  fetchOptionSet: PropTypes.func.isRequired
}

export default OptionSets
