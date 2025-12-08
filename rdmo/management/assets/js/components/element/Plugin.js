import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { siteId } from 'rdmo/core/assets/js/utils/meta'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { AvailableLink, CodeLink, CopyLink, EditLink, LockedLink, ToggleCurrentSiteLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const Plugin = ({ config, plugin, elementActions, filter=false, filterSites=false, filterEditors=false }) => {
  const showElement = filterElement(config, filter, filterSites, filterEditors, plugin)

  const editUrl = buildPath('plugins', plugin.id)
  const copyUrl = buildPath('plugins', plugin.id, 'copy')

  const fetchEdit = () => elementActions.fetchElement('plugins', plugin.id)
  const fetchCopy = () => elementActions.fetchElement('plugins', plugin.id, 'copy')
  const toggleAvailable = () => elementActions.storeElement('plugins', {...plugin, available: !plugin.available })
  const toggleLocked = () => elementActions.storeElement('plugins', {...plugin, locked: !plugin.locked })
  const toggleCurrentSite = () => elementActions.storeElement('plugins', plugin, 'toggle-site')

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This plugin is read only')} show={plugin.read_only} />
          <EditLink title={gettext('Edit plugin')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy plugin')} href={copyUrl} onClick={fetchCopy} />
          <AvailableLink title={plugin.available ? gettext('Make plugin unavailable')
                                               : gettext('Make plugin available')}
                         available={plugin.available} locked={plugin.locked} onClick={toggleAvailable}
                         disabled={plugin.read_only} />
          <ToggleCurrentSiteLink hasCurrentSite={config.settings.multisite ? plugin.sites.includes(siteId) : true}
                         onClick={toggleCurrentSite}
                         show={config.settings.multisite}/>
          <LockedLink title={plugin.locked ? gettext('Unlock plugin') : gettext('Lock plugin')}
                      locked={plugin.locked} onClick={toggleLocked} disabled={plugin.read_only} />
        </div>
        <div>
          <p>
            <strong>{gettext('Plugin')}{': '}</strong>
            <span dangerouslySetInnerHTML={{ __html: plugin.title }}></span>
          </p>
          {
            get(config, 'display.uri.plugins', true) && <p>
              <CodeLink className="code-config" uri={plugin.uri} href={editUrl} onClick={() => fetchEdit()} />
            </p>
          }
          <p>
            <strong>{gettext('Type')}{': '}</strong>
            <code className="code-config">{plugin.plugin_type || gettext('Unknown')}</code>
          </p>
          <ElementErrors element={plugin} />
        </div>
      </div>
    </li>
  )
}

Plugin.propTypes = {
  config: PropTypes.object.isRequired,
  plugin: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  filter: PropTypes.string,
  filterSites: PropTypes.bool,
  filterEditors: PropTypes.bool
}

export default Plugin
