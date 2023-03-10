import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Sections = ({ config, sections, fetchSection, storeSection }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchSection(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Sections')} />

      <ul className="list-group">
      {
        filterElements(config, sections).map((section, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="element-options">
                <EditLink element={section} verboseName={gettext('section')}
                          onClick={section => fetchSection(section.id)} />
                <LockedLink element={section} verboseName={gettext('section')}
                            onClick={locked => storeSection(Object.assign({}, section, { locked }))} />
                <ExportLink element={section} verboseName={gettext('section')} />
              </div>
              <div>
                <p>
                  <strong>{gettext('Section')}{': '}</strong> {section.title}
                </p>
                <p>
                  <code className="code-questions">{section.uri}</code>
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

Sections.propTypes = {
  config: PropTypes.object.isRequired,
  sections: PropTypes.array.isRequired,
  fetchSection: PropTypes.func.isRequired,
  storeSection: PropTypes.func.isRequired
}

export default Sections
