import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import get from 'lodash/get'

import Html from 'rdmo/core/assets/js/components/Html'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'
import { siteId } from 'rdmo/core/assets/js/utils/meta'

import { fetchElement, storeElement } from '../../actions/elementActions'

import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, AvailableLink, LockedLink, ExportLink, CodeLink, ToggleCurrentSiteLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const View = ({ view, filter=false, filterSites=false, filterEditors=false }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, filterSites, filterEditors, view)

  const editUrl = buildPath('views', view.id)
  const copyUrl = buildPath('views', view.id, 'copy')
  const exportUrl = buildApiPath('views', 'views', view.id, 'export')

  const fetchEdit = () => dispatch(fetchElement('views', view.id))
  const fetchCopy = () => dispatch(fetchElement('views', view.id, 'copy'))
  const toggleAvailable = () => dispatch(storeElement('views', {...view, available: !view.available }))
  const toggleLocked = () => dispatch(storeElement('views', {...view, locked: !view.locked }))
  const toggleCurrentSite = () => dispatch(storeElement('views', view, 'toggle-site'))

  const displayUriViews = isTruthy(get(config, 'display.uri.views', true))

  return showElement && (
    <li className="list-group-item">
      <div className="d-flex flex-column gap-2">
        <div className="d-flex align-items-center gap-2">
          <strong>{gettext('View')}{':'}</strong>
          <div className="flex-grow-1">
            <Html html={view.title} />
          </div>

          <div className="d-flex align-items-center gap-1">
            <ReadOnlyIcon title={gettext('This view is read only')} show={view.read_only} />
            <EditLink title={gettext('Edit view')} href={editUrl} onClick={fetchEdit} />
            <CopyLink title={gettext('Copy view')} href={copyUrl} onClick={fetchCopy} />
            <AvailableLink title={view.available ? gettext('Make view unavailable')
                                                 : gettext('Make view available')}
                           available={view.available} locked={view.locked} onClick={toggleAvailable}
                           disabled={view.read_only} />
            <ToggleCurrentSiteLink hasCurrentSite={config.settings.multisite ? view.sites.includes(siteId) : true}
                           onClick={toggleCurrentSite}
                           show={config.settings.multisite}/>
            <LockedLink title={view.locked ? gettext('Unlock view') : gettext('Lock view')}
                        locked={view.locked} onClick={toggleLocked} disabled={view.read_only} />
            <ExportLink title={gettext('Export view')} exportUrl={exportUrl}
                        exportFormats={config.settings.export_formats} />
          </div>
        </div>
        {
          displayUriViews && (
            <CodeLink type="views" uri={view.uri} href={editUrl} onClick={() => fetchEdit()} />
          )
        }
        <ElementErrors element={view} />
      </div>
    </li>
  )
}

View.propTypes = {
  view: PropTypes.object.isRequired,
  filter: PropTypes.string,
  filterSites: PropTypes.bool,
  filterEditors: PropTypes.bool
}

export default View
