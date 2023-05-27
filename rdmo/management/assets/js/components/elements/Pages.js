import React from 'react'
import PropTypes from 'prop-types'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Page from '../element/Page'

const Pages = ({ config, pages, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.pages.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.pages.uri_prefix', value)
  const updateDisplayPagesURI = (value) => configActions.updateConfig('display.uri.pages', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)

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
            <FilterString value={config.filter.pages.search} onChange={updateFilterString}
                          placeholder={gettext('Filter pages')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={config.filter.pages.uri_prefix} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(pages)} />
          </div>
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Pages')}</code>}
                    value={config.display.uri.pages} onChange={updateDisplayPagesURI} />
          <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                    value={config.display.uri.attributes} onChange={updateDisplayAttributesURI} />
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
