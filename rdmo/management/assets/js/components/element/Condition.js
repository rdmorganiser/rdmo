import React from 'react'
import PropTypes from 'prop-types'

import { filterElement } from '../../utils/filter'
import { buildPath } from '../../utils/location'

import { ElementErrors } from '../common/Errors'
import { EditLink, CopyLink, LockedLink, ExportLink, CodeLink } from '../common/Links'
import { ReadOnlyIcon } from '../common/Icons'

const Condition = ({ config, condition, elementActions, filter=false, filterEditors=false }) => {

  const showElement = filterElement(config, filter, false, filterEditors, condition)

  const editUrl = buildPath(config.baseUrl, 'conditions', condition.id)
  const copyUrl = buildPath(config.baseUrl, 'conditions', condition.id, 'copy')
  const exportUrl = buildPath('/api/v1/', 'conditions', 'conditions', condition.id, 'export')

  const fetchEdit = () => elementActions.fetchElement('conditions', condition.id)
  const fetchCopy = () => elementActions.fetchElement('conditions', condition.id, 'copy')
  const toggleLocked = () => elementActions.storeElement('conditions', {...condition, locked: !condition.locked })

  return showElement && (
    <li className="list-group-item">
      <div className="element">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This condition is read only')} show={condition.read_only} />
          <EditLink title={gettext('Edit condition')} href={editUrl} onClick={fetchEdit} />
          <CopyLink title={gettext('Copy condition')} href={copyUrl} onClick={fetchCopy} />
          <LockedLink title={condition.locked ? gettext('Unlock condition') : gettext('Lock condition')}
                      locked={condition.locked} onClick={toggleLocked} disabled={condition.read_only} />
          <ExportLink title={gettext('Export condition')} exportUrl={exportUrl}
                      exportFormats={config.settings.export_formats} full={true} />
        </div>
        <div>
          <p>
            <strong>{gettext('Condition')}{': '}</strong>
            <CodeLink className="code-conditions" uri={condition.uri} onClick={() => fetchEdit()} />
          </p>
          <ElementErrors element={condition} />
        </div>
      </div>
    </li>
  )
}

Condition.propTypes = {
  config: PropTypes.object.isRequired,
  condition: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  filter: PropTypes.string,
  filterEditors: PropTypes.bool
}

export default Condition
