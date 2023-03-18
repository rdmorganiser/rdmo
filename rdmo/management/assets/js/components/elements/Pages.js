import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Page from '../element/Page'
import ElementButtons from '../common/ElementButtons'

const Pages = ({ config, pages, fetchElement, createElement, storeElement }) => {

  const createPage = () => createElement('pages')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <ElementButtons onCreate={createPage} />
        <strong>{gettext('Pages')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, pages).map((page, index) => (
          <Page key={index} config={config} page={page}
                fetchElement={fetchElement} storeElement={storeElement} />
        ))
      }
      </ul>
    </div>
  )
}

Pages.propTypes = {
  config: PropTypes.object.isRequired,
  pages: PropTypes.array.isRequired,
  fetchElement: PropTypes.func.isRequired,
  createElement: PropTypes.func.isRequired,
  storeElement: PropTypes.func.isRequired
}

export default Pages
