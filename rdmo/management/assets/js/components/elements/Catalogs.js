import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

const Catalogs = ({ config, catalogs, fetchCatalog }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchCatalog(id)
  }

  return (
    <div className="catalogs">
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
          </div>
          <div>
            <strong>{gettext('Catalogs')}</strong>
          </div>
        </div>
      </div>
      {
        filterElements(config, catalogs).map((catalog, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
                <div className="pull-right">
                  <a href="" className="fa fa-pencil"
                     title={gettext('Edit catalog')}
                     onClick={event => handleEdit(event, catalog.id)}>
                  </a>
                  {' '}
                  <a href={catalog.xml_url} className="fa fa-download"
                     title={gettext('Export catalog as XML')}
                     target="blank">
                  </a>
                </div>
                <div>
                  <strong>{gettext('Catalog')}</strong>
                  {' '}
                  <span>{catalog.title}</span>
                </div>
              </div>
              <div className="panel-body">
                <strong>{gettext('URI')}:</strong>
                {' '}
                <code className="code-questions">{catalog.uri}</code>
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

Catalogs.propTypes = {
  config: PropTypes.object.isRequired,
  catalogs: PropTypes.array.isRequired,
  fetchCatalog: PropTypes.func.isRequired
}

export default Catalogs
