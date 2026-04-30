import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { getUriPrefixes } from '../../utils/filter'

import { FilterString, FilterUriPrefix, FilterSite} from '../common/Filter'
import { BackButton, NewButton } from '../common/Buttons'
import { Checkbox } from '../common/Checkboxes'

import Plugin from '../element/Plugin'

const Plugins = ({ config, plugins, configActions, elementActions }) => {

  const updateFilterString = (value) => configActions.updateConfig('filter.plugins.search', value)
  const updateFilterUriPrefix = (value) => configActions.updateConfig('filter.plugins.uri_prefix', value)
  const updateFilterSite = (value) => configActions.updateConfig('filter.sites', value)
  const updateFilterEditor = (value) => configActions.updateConfig('filter.editors', value)

  const updateDisplayPluginsURI = (value) => configActions.updateConfig('display.uri.plugins', value)

  const createPlugin = () => elementActions.createElement('plugins')

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <NewButton onClick={createPlugin} />
        </div>
        <strong>{gettext('Plugins')}</strong>
      </div>

      <div className="panel-body">
        <div className="row">
          <div className={config.settings.multisite ? 'col-sm-4' : 'col-sm-8'}>
            <FilterString value={get(config, 'filter.plugins.search', '')} onChange={updateFilterString}
                          label={gettext('Filter plugins')} />
          </div>
          <div className="col-sm-4">
            <FilterUriPrefix value={get(config, 'filter.plugins.uri_prefix', '')} onChange={updateFilterUriPrefix}
                             options={getUriPrefixes(plugins)} />
          </div>
          {
            config.settings.multisite && <>
              <div className="col-sm-2">
                <FilterSite value={get(config, 'filter.sites', '')} onChange={updateFilterSite}
                            options={config.sites} />
              </div>
              <div className="col-sm-2">
                <FilterSite value={get(config, 'filter.editors', '')} onChange={updateFilterEditor}
                            options={config.sites} label={gettext('Filter editors')} allLabel={gettext('All editors')} />
              </div>
            </>
          }
        </div>
        <div className="checkboxes">
          <span className="mr-10">{gettext('Show URIs:')}</span>
          <Checkbox label={<code className="code-config">{gettext('Plugins')}</code>}
                    value={get(config, 'display.uri.plugins', true)} onChange={updateDisplayPluginsURI} />
        </div>

      </div>

      <ul className="list-group">
      {
        plugins.map((plugin, index) => (
          <Plugin key={index} config={config} plugin={plugin}
                  elementActions={elementActions}
                  filter="plugins" filterSites={true} filterEditors={true} />
        ))
      }
      </ul>
    </div>
  )
}

Plugins.propTypes = {
  config: PropTypes.object.isRequired,
  plugins: PropTypes.array.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default Plugins
