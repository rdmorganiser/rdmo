import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

const Pages = ({ config, pages, fetchPage }) => {
  const handleEdit = (event, id) => {
    event.preventDefault()
    fetchPage(id)
  }

  return (
    <div className="pages">
      <div className="panel panel-default">
        <div className="panel-heading">
          <div className="pull-right">
            <button className="btn btn-xs btn-default" onClick={event => history.back()}>
              {gettext('Back')}
            </button>
          </div>
          <div>
            <strong>{gettext('Pages')}</strong>
          </div>
        </div>
      </div>
      {
        filterElements(config, pages).map((page, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
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
                  <strong>{gettext('Page')}</strong>
                  {' '}
                  <span>{page.text}</span>
                </div>
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

Pages.propTypes = {
  config: PropTypes.object.isRequired,
  pages: PropTypes.array.isRequired,
  fetchPage: PropTypes.func.isRequired
}

export default Pages
