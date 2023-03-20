import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { filterElements } from '../../utils/filter'

import Page from '../element/Page'
import { BackButton, NewButton } from '../common/ElementButtons'

const Pages = ({ config, pages, elementActions }) => {

  const createPage = () => elementActions.createElement('pages')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createPage} />
        </div>
        <strong>{gettext('Pages')}</strong>
      </div>

      <ul className="list-group">
      {
        filterElements(config, pages).map((page, index) => (
          <Page key={index} config={config} page={page}
                elementActions={elementActions} />
        ))
      }
      </ul>
    </div>
  )
}

Pages.propTypes = {
  config: PropTypes.object.isRequired,
  pages: PropTypes.array.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Pages
