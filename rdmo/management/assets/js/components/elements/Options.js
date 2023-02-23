import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Options = ({ config, options, fetchOption }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchOption(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Catalogs')} />
      <ul className="list-group">
      {
        filterElements(config, options).map((option, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit option')}
                   onClick={event => handleEdit(event, option.id)}>
                </a>
                {' '}
                <a href={option.xml_url} className="fa fa-download"
                   title={gettext('Export option as XML')}
                   target="blank">
                </a>
              </div>
              <div>
                <p>
                  <strong>{gettext('Option')}{': '}</strong> {option.text}
                </p>
                <p>
                  <code className="code-options">{option.uri}</code>
                </p>
              </div>
            </li>
          )
        })
      }
      </ul>
    </div>
  )
}

Options.propTypes = {
  config: PropTypes.object.isRequired,
  options: PropTypes.array.isRequired,
  fetchOption: PropTypes.func.isRequired
}

export default Options
