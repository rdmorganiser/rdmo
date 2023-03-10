import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, LockedLink, ExportLink } from '../common/ElementLinks'

const OptionSets = ({ config, optionsets, fetchOptionSet, storeOptionSet }) => {
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
              <div className="element-options">
                <EditLink element={optionset} verboseName={gettext('optionset')}
                          onClick={optionset => fetchOptionSet(optionset.id)} />
                <LockedLink element={optionset} verboseName={gettext('optionset')}
                            onClick={locked => storeOptionSet(Object.assign({}, optionset, { locked }))} />
                <ExportLink element={optionset} verboseName={gettext('optionset')} />
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
  fetchOptionSet: PropTypes.func.isRequired,
  storeOptionSet: PropTypes.func.isRequired
}

export default OptionSets
