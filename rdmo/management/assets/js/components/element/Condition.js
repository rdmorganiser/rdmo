import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import { fetchElement, storeElement } from '../../actions/elementActions'
import { filterElement } from '../../utils/filter'
import { buildApiPath, buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { ReadOnlyIcon } from '../common/Icons'
import { CodeLink, CopyLink, EditLink, ExportLink, LockedLink } from '../common/Links'

const Condition = ({ condition, filter = false, filterEditors = false }) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)

  const showElement = filterElement(config, filter, false, filterEditors, condition)

  const editUrl = buildPath('conditions', condition.id)
  const copyUrl = buildPath('conditions', condition.id, 'copy')
  const exportUrl = buildApiPath('conditions', 'conditions', condition.id, 'export')

  const fetchEdit = () => dispatch(fetchElement('conditions', condition.id))
  const fetchCopy = () => dispatch(fetchElement('conditions', condition.id, 'copy'))
  const toggleLocked = () => dispatch(storeElement('conditions', {...condition, locked: !condition.locked }))

  return showElement && (
    <li className="list-group-item">
      <div className="d-flex flex-column gap-2">
        <div className="d-flex align-items-center gap-2">
          <strong>{gettext('Condition')}{':'}</strong>
          <CodeLink
            className="flex-grow-1" type="conditions" uri={condition.uri} href={editUrl}
            onClick={() => fetchEdit()} />

          <div className="d-flex align-items-center gap-1">
            <ReadOnlyIcon title={gettext('This condition is read only')} show={condition.read_only} />
            <EditLink title={gettext('Edit condition')} href={editUrl} onClick={fetchEdit} />
            <CopyLink title={gettext('Copy condition')} href={copyUrl} onClick={fetchCopy} />
            <LockedLink
              title={condition.locked ? gettext('Unlock condition') : gettext('Lock condition')}
              locked={condition.locked} onClick={toggleLocked} disabled={condition.read_only} />
            <ExportLink
              title={gettext('Export condition')} exportUrl={exportUrl}
              exportFormats={config.settings.export_formats} full={true} />
          </div>
        </div>
        <ElementErrors element={condition} />
      </div>
    </li>
  )
}

Condition.propTypes = {
  condition: PropTypes.object.isRequired,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool
}

export default Condition
