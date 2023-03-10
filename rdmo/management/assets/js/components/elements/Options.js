import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Options = ({ config, options, fetchOption, storeOption }) => {
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
              <div className="element-options">
                <EditLink element={option} verboseName={gettext('option')}
                          onClick={option => fetchOption(option.id)} />
                <LockedLink element={option} verboseName={gettext('option')}
                            onClick={locked => storeOption(Object.assign({}, option, { locked }))} />
                <ExportLink element={option} verboseName={gettext('option')} />
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
  fetchOption: PropTypes.func.isRequired,
  storeOption: PropTypes.func.isRequired
}

export default Options
