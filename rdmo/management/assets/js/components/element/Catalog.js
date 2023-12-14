import React from 'react'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, AvailableLink, ToggleCurrentSiteLink, LockedLink, NestedLink,
         ExportLink, CodeLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const Catalog = ({ config, catalog, elementActions, display='list',
                   filter=false, filterSites=false, filterEditors=false }) => {

  const showElement = filterElement(config, filter, filterSites, filterEditors, catalog)

  const editUrl = buildPath(config.baseUrl, 'catalogs', catalog.id)
  const copyUrl = buildPath(config.baseUrl, 'catalogs', catalog.id, 'copy')
  const nestedUrl = buildPath(config.baseUrl, 'catalogs', catalog.id, 'nested')
  const exportUrl = buildPath(config.apiUrl, 'questions', 'catalogs', catalog.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('catalogs', catalog.id)
  const fetchCopy = () => elementActions.fetchElement('catalogs', catalog.id, 'copy')
  const fetchNested = () => elementActions.fetchElement('catalogs', catalog.id, 'nested')

  const toggleAvailable = () => elementActions.storeElement('catalogs', {...catalog, available: !catalog.available })
  const toggleLocked = () => elementActions.storeElement('catalogs', {...catalog, locked: !catalog.locked })
  const addCurrentSite = () => elementActions.storeElement('catalogs', catalog, null, 'add-site')
  const removeCurrentSite = () => elementActions.storeElement('catalogs', catalog, null, 'remove-site')
  let has_current_site =  config.settings.multisite ? catalog.sites.includes(config.currentSite.id) : true
  const createSection = () => elementActions.createElement('sections', { catalog })

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ToggleCurrentSiteLink has_current_site={has_current_site}
                    locked={catalog.locked} onClick={has_current_site ? removeCurrentSite : addCurrentSite}
                    show={config.settings.multisite}/>
        <ReadOnlyIcon title={gettext('This catalog is read only')} show={catalog.read_only} />
        <NestedLink title={gettext('View catalog nested')} href={nestedUrl} onClick={fetchNested} />
        <EditLink title={gettext('Edit catalog')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy catalog')} href={copyUrl} onClick={fetchCopy} />
        <AddLink title={gettext('Add section')} onClick={createSection} disabled={catalog.read_only} />
        <AvailableLink title={catalog.available ? gettext('Make catalog unavailable')
                                                : gettext('Make catalog available')}
                       available={catalog.available} locked={catalog.locked} onClick={toggleAvailable}
                       disabled={catalog.read_only} />
        <LockedLink title={catalog.locked ? gettext('Unlock catalog') : gettext('Lock catalog')}
                    locked={catalog.locked} onClick={toggleLocked} disabled={catalog.read_only} />
        <ExportLink title={gettext('Export catalog')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} full={true} />
      </div>
      <div>
        <p>
          <strong>{gettext('Catalog')}{': '}</strong> {catalog.title}
        </p>
        {
          get(config, 'display.uri.catalogs', true) &&
          <CodeLink className="code-questions" uri={catalog.uri} onClick={() => fetchEdit()} />
        }
        <ElementErrors element={catalog} />
      </div>
    </div>
  )

  switch (display) {
    case 'list':
      return showElement && (
        <li className="list-group-item">
          { elementNode }
        </li>
      )
    case 'plain':
      return elementNode
  }
}

Catalog.propTypes = {
  config: PropTypes.object.isRequired,
  catalog: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.string,
  filterSites: PropTypes.bool,
  filterEditors: PropTypes.bool
}

export default Catalog
