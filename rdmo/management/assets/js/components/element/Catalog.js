import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import { siteId } from 'rdmo/core/assets/js/utils/meta'

import { fetchElement, storeElement, createElement } from '../../actions/elementActions'

import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AddLink, AvailableLink, ToggleCurrentSiteLink, LockedLink, NestedLink,
         ExportLink, CodeLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const Catalog = ({ catalog, display='list', filter=false, filterSites=false, filterEditors=false }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, filterSites, filterEditors, catalog)

  const editUrl = buildPath('catalogs', catalog.id)
  const copyUrl = buildPath('catalogs', catalog.id, 'copy')
  const nestedUrl = buildPath('catalogs', catalog.id, 'nested')
  const exportUrl = buildApiPath('questions', 'catalogs', catalog.id, 'export')

  const fetchEdit = () => dispatch(fetchElement('catalogs', catalog.id))
  const fetchCopy = () => dispatch(fetchElement('catalogs', catalog.id, 'copy'))
  const fetchNested = () => dispatch(fetchElement('catalogs', catalog.id, 'nested'))

  const toggleAvailable = () => dispatch(storeElement('catalogs', {...catalog, available: !catalog.available }))
  const toggleLocked = () => dispatch(storeElement('catalogs', {...catalog, locked: !catalog.locked }))

  const toggleCurrentSite = () => dispatch(storeElement('catalogs', catalog, 'toggle-site'))

  const createSection = () => dispatch(createElement('sections', { catalog }))

  const elementNode = (
    <div className="element">
      <div className="pull-right">
        <ReadOnlyIcon title={gettext('This catalog is read only')} show={catalog.read_only} />
        <NestedLink title={gettext('View catalog nested')} href={nestedUrl} onClick={fetchNested} />
        <EditLink title={gettext('Edit catalog')} href={editUrl} onClick={fetchEdit} />
        <CopyLink title={gettext('Copy catalog')} href={copyUrl} onClick={fetchCopy} />
        <AddLink title={gettext('Add section')} onClick={createSection} disabled={catalog.read_only} />
        <AvailableLink title={catalog.available ? gettext('Make catalog unavailable')
                                                : gettext('Make catalog available')}
                       available={catalog.available} locked={catalog.locked} onClick={toggleAvailable}
                       disabled={catalog.read_only} />
        <ToggleCurrentSiteLink hasCurrentSite={config.settings.multisite ? catalog.sites.includes(siteId) : true}
                       onClick={toggleCurrentSite}
                       show={config.settings.multisite}/>
        <LockedLink title={catalog.locked ? gettext('Unlock catalog') : gettext('Lock catalog')}
                    locked={catalog.locked} onClick={toggleLocked} disabled={catalog.read_only} />
        <ExportLink title={gettext('Export catalog')} exportUrl={exportUrl}
                    exportFormats={config.settings.export_formats} full={true} />
      </div>
      <div>
        <p>
          <strong>{gettext('Catalog')}{': '}</strong>
          <span dangerouslySetInnerHTML={{ __html: catalog.title }}></span>
        </p>
        {
          get(config, 'display.uri.catalogs', true) &&
          <CodeLink className="code-questions" uri={catalog.uri} href={editUrl} onClick={() => fetchEdit()} />
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
  catalog: PropTypes.object.isRequired,
  display: PropTypes.string,
  filter: PropTypes.string,
  filterSites: PropTypes.bool,
  filterEditors: PropTypes.bool
}

export default Catalog
