import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Catalogs = ({ catalogs }) => {
  return (
    <div className="catalogs">
      <div className="panel panel-default">
        <div className="panel-body">
          <strong>Catalogs</strong>
        </div>
      </div>
      {
        catalogs.map((catalog, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
                <strong>Catalog</strong> {catalog.title}
              </div>
              <div className="panel-body">
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
  catalogs: PropTypes.array.isRequired
}

export default Catalogs
