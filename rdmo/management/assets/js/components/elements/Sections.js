import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Sections = ({ config, sections, fetchSection }) => {
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
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit section')}
                   onClick={event => handleEdit(event, section.id)}>
                </a>
                {' '}
                <a href={section.xml_url} className="fa fa-download"
                   title={gettext('Export section as XML')}
                   target="blank">
                </a>
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
}

export default Sections
