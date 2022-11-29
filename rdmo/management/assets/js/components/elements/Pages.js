import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

const Pages = ({ config, pages }) => {
  return (
    <div className="pages">
      <div className="panel panel-default">
        <div className="panel-body">
          <strong>Pages</strong>
        </div>
      </div>
      {
        filterElements(config, pages).map((page, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
                <strong>Page</strong> {page.title}
              </div>
              <div className="panel-body">
                <code className="code-questions">{page.uri}</code>
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

Pages.propTypes = {
  pages: PropTypes.array.isRequired
}

export default Pages
