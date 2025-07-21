import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite } from '../common/Filter'
import { Checkbox } from '../common/Checkboxes'
import { BackButton, NewButton } from '../common/Buttons'

import Page from '../element/Page'

const Pages = ({ config, pages, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.pages.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.pages.uri_prefix', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.editors', value)

  const updateDisplayPagesURI = (value) => configActions.updateConfig('display.uri.pages', value)
  const updateDisplayAttributesURI = (value) => configActions.updateConfig('display.uri.attributes', value)
  const updateDisplayConditionsURI = (value) => configActions.updateConfig('display.uri.conditions', value)

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
          <div className={config.settings.multisite ? 'col-sm-6' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.pages.search', '')} onChange={updateFilterString}
                          label={gettext('Filter pages')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.pages.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(pages)} />
          </div>
          {
            config.settings.multisite && <div className="col-sm-2">
              <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                          options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
            </div>
          }
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-questions">{gettext('Pages')}</code>}
                    value={get(config, 'display.uri.pages', true)} onChange={updateDisplayPagesURI} />
          <Checkbox label={<code className="code-domain">{gettext('Attributes')}</code>}
                    value={get(config, 'display.uri.attributes', true)} onChange={updateDisplayAttributesURI} />
          <Checkbox label={<code className="code-conditions">{gettext('Conditions')}</code>}
                    value={get(config, 'display.uri.conditions', true)} onChange={updateDisplayConditionsURI} />
        </div>
      </div>

      <ul className="list-group">
      {
        pages.map((page, index) => (
          <Page key={index} config={config} page={page}
                configActions={configActions} elementActions={elementActions}
                filter="pages" filterEditors={true} />
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
