import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'

const Pages = ({ config, pages, fetchPage }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchPage(id)
  }

  return (
    <div className="panel panel-default">
      <ElementsHeading verboseName={gettext('Catalogs')} />
      <ul className="list-group">
      {
        filterElements(config, pages).map((page, index) => {
          return (
            <li key={index} className="list-group-item">
              <div className="pull-right">
                <a href="" className="fa fa-pencil"
                   title={gettext('Edit page')}
                   onClick={event => handleEdit(event, page.id)}>
                </a>
                {' '}
                <a href={page.xml_url} className="fa fa-download"
                   title={gettext('Export pages as XML')}
                   target="blank">
                </a>
              </div>
              <div>
                <p>
                  <strong>{gettext('Page')}{': '}</strong> {page.title}
                </p>
                <p>
                  <code className="code-questions">{page.uri}</code>
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

Pages.propTypes = {
  config: PropTypes.object.isRequired,
  pages: PropTypes.array.isRequired,
  fetchPage: PropTypes.func.isRequired
}

export default Pages
