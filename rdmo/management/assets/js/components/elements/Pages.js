import React, { Component} from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import FilterUri from '../FilterUri'
import FilterUriPrefix from '../FilterUriPrefix'

import Page from '../element/Page'
import { BackButton, NewButton } from '../common/ElementButtons'

const Pages = ({ config, pages, configActions, elementActions }) => {

  const updateFilterUri = (uri) => configActions.updateConfig('filter.pages.uri', uri)
  const updateFilterUriPrefix = (uriPrefix) => configActions.updateConfig('filter.pages.uriPrefix', uriPrefix)

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

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-8">
            <FilterUri value={config.filter.pages.uri} onChange={updateFilterUri}
                       placeholder={gettext('Filter pages by URI')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.pages.uriPrefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(pages)} />
          </div>
        </div>
      </div>

      <ul className="list-group">
      {
        pages.map((page, index) => (
          <Page key={index} config={config} page={page} elementActions={elementActions}
                filter={config.filter.pages} />
        ))
      }
      </ul>
    </div>
  )
}

Pages.propTypes = {
  config: PropTypes.object.isRequired,
  pages: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Pages
