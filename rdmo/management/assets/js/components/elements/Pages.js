import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import ElementsHeading from '../common/ElementsHeading'
import { EditLink, LockedLink, ExportLink } from '../common/ElementLinks'

const Pages = ({ config, pages, fetchPage, storePage }) => {
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
              <div className="element-options">
                <EditLink element={page} verboseName={gettext('page')}
                          onClick={page => fetchPage(page.id)} />
                <LockedLink element={page} verboseName={gettext('page')}
                            onClick={locked => storePage(Object.assign({}, page, { locked }))} />
                <ExportLink element={page} verboseName={gettext('page')} />
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
  fetchPage: PropTypes.func.isRequired,
  storePage: PropTypes.func.isRequired
}

export default Pages
