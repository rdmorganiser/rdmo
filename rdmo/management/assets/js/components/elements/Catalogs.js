import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Catalogs = ({ config, catalogs, fetchCatalog }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchCatalog(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Catalogs')} />
      <ul className="list-group">
      {
        filterElements(config, catalogs).map((catalog, index) => {
          return (
            <li key={index} className="list-group-item">
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
                <p>
                  <strong>{gettext('Catalog')}{': '}</strong> {catalog.title}
                </p>
                <p>
                  <code className="code-questions">{catalog.uri}</code>
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

Catalogs.propTypes = {
  config: PropTypes.object.isRequired,
  catalogs: PropTypes.array.isRequired,
  fetchCatalog: PropTypes.func.isRequired
}

export default Catalogs
