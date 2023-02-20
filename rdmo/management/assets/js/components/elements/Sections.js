import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

const Sections = ({ config, sections, fetchSection }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchSection(id)
  }

  return (
    <div className="sections">
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
          </div>
          <div>
            <strong>{gettext('Sections')}</strong>
          </div>
        </div>
      </div>
      {
        filterElements(config, sections).map((section, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
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
                  <strong>{gettext('Section')}:</strong>
                  {' '}
                  <span>{section.title}</span>
                </div>
              </div>
              <div className="panel-body">
                <strong>{gettext('URI')}:</strong>
                {' '}
                <code className="code-questions">{section.uri}</code>
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

Sections.propTypes = {
  config: PropTypes.object.isRequired,
  sections: PropTypes.array.isRequired,
  fetchSection: PropTypes.func.isRequired,
}

export default Sections
